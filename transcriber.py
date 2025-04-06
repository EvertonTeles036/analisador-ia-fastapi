
import os
import requests
from pydub import AudioSegment
from fpdf import FPDF

API_KEY = "d7f4166d1399467a95aac2d8ef4e8421"

def dividir_audio(caminho, duracao_maxima_ms=600000):
    audio = AudioSegment.from_file(caminho)
    partes = []
    for i in range(0, len(audio), duracao_maxima_ms):
        parte = audio[i:i+duracao_maxima_ms]
        nome_parte = f"{caminho}_parte{i//duracao_maxima_ms}.mp3"
        parte.export(nome_parte, format="mp3")
        partes.append(nome_parte)
    return partes

def transcrever_audio(caminho_audio):
    headers = {"authorization": API_KEY}
    with open(caminho_audio, "rb") as f:
        response = requests.post("https://api.assemblyai.com/v2/upload", headers=headers, files={"file": f})
    upload_url = response.json()["upload_url"]
    
    json = { "audio_url": upload_url }
    response = requests.post("https://api.assemblyai.com/v2/transcript", json=json, headers=headers)
    transcript_id = response.json()["id"]
    
    while True:
        polling = requests.get(f"https://api.assemblyai.com/v2/transcript/{transcript_id}", headers=headers)
        status = polling.json()["status"]
        if status == "completed":
            return polling.json()["text"]
        elif status == "error":
            return "Erro na transcrição"

def salvar_pdf(nome_base, texto):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, texto)
    nome_pdf = f"{nome_base}.pdf"
    pdf.output(nome_pdf)

def transcrever_arquivos(arquivos):
    resultados = {}
    for arquivo in arquivos:
        caminho = f"temp_{arquivo.filename}"
        with open(caminho, "wb") as buffer:
            buffer.write(arquivo.file.read())

        partes = dividir_audio(caminho)
        transcricao_total = ""
        for parte in partes:
            texto = transcrever_audio(parte)
            transcricao_total += texto + "\n"
            os.remove(parte)
        salvar_pdf(arquivo.filename.split('.')[0], transcricao_total)
        resultados[arquivo.filename] = "Transcrição finalizada"
        os.remove(caminho)
    return resultados

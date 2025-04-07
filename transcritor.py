import requests
import time
import os
from fpdf import FPDF

# Insira sua chave da AssemblyAI
API_KEY_ASSEMBLYAI = "d7f4166d1399467a95aac2d8ef4e8421"
HEADERS = {
    "authorization": API_KEY_ASSEMBLYAI,
    "content-type": "application/json"
}

# Cria pasta local para PDF (se não existir)
os.makedirs("pdfs", exist_ok=True)

def transcrever_audio(nome_arquivo, url_audio):
    print(f"Iniciando transcrição do arquivo: {nome_arquivo}")

    # Envia URL para AssemblyAI
    response = requests.post(
        "https://api.assemblyai.com/v2/transcript",
        headers=HEADERS,
        json={"audio_url": url_audio, "language_code": "pt"}
    )

    if response.status_code != 200:
        raise Exception(f"Erro ao iniciar transcrição: {response.text}")

    transcript_id = response.json()["id"]

    # Consulta até a transcrição estar pronta
    while True:
        status_response = requests.get(
            f"https://api.assemblyai.com/v2/transcript/{transcript_id}",
            headers=HEADERS
        )
        status = status_response.json()["status"]
        if status == "completed":
            break
        elif status == "error":
            raise Exception(f"Erro na transcrição: {status_response.json()['error']}")
        time.sleep(5)

    texto = status_response.json()["text"]

    # Geração do PDF com mesmo nome do áudio
    nome_pdf = nome_arquivo.rsplit(".", 1)[0] + ".pdf"
    caminho_pdf = os.path.join("pdfs", nome_pdf)

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    linhas = texto.split("\n")
    for linha in linhas:
        pdf.multi_cell(0, 10, linha)

    pdf.output(caminho_pdf)

    print(f"Transcrição salva em: {caminho_pdf}")
    return nome_pdf

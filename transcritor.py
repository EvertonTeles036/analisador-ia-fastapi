import requests
import time
import os
import sys

# Verificação e instalação automática da fpdf
try:
    from fpdf import FPDF
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "fpdf"])
    from fpdf import FPDF

# ✅ SUA CHAVE ASSEMBLYAI
API_KEY_ASSEMBLYAI = "df741661d399467a95aac2d8ef4e8421"
HEADERS = {
    "authorization": API_KEY_ASSEMBLYAI,
    "content-type": "application/json"
}

# 🔁 URL assinada do GCS (troque pelo áudio que deseja transcrever)
AUDIO_URL = "COLE_AQUI_SUA_URL_ASSINADA_DO_AUDIO"

# Envia o áudio para a API da AssemblyAI
response = requests.post(
    "https://api.assemblyai.com/v2/transcript",
    headers=HEADERS,
    json={"audio_url": AUDIO_URL}
)

transcription_id = response.json()["id"]

# Acompanha o progresso da transcrição
status = "queued"
while status not in ["completed", "error"]:
    status_response = requests.get(
        f"https://api.assemblyai.com/v2/transcript/{transcription_id}",
        headers=HEADERS
    )
    status = status_response.json()["status"]
    if status == "error":
        print("Erro na transcrição:", status_response.json()["error"])
        break
    elif status != "completed":
        time.sleep(5)

# Processa o texto transcrito
texto = status_response.json().get("text", "")
nome_arquivo = AUDIO_URL.split("/")[-1].split("?")[0].split(".")[0]
pdf_nome = f"{nome_arquivo}.pdf"

# Cria o PDF com o texto transcrito
pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=12)

linhas = texto.split(". ")
for linha in linhas:
    pdf.multi_cell(0, 10, linha.strip() + ".", align='L')

pdf.output(pdf_nome)
print(f"✅ Transcrição salva em: {pdf_nome}")

import requests
import time
import os
from fpdf import FPDF
from dotenv import load_dotenv

# Carrega variáveis do arquivo .env
load_dotenv()

# Pega a API Key de uma variável de ambiente
API_KEY = os.getenv("ASSEMBLYAI_API_KEY")

# Verifica se a chave foi encontrada
if not API_KEY:
    raise ValueError("API Key da AssemblyAI não encontrada. Verifique se a variável ASSEMBLYAI_API_KEY está definida no .env")

# URL base da API AssemblyAI
BASE_URL = "https://api.assemblyai.com/v2"

# Nome do arquivo de áudio no bucket (pode ser ajustado dinamicamente se necessário)
audio_url = "https://storage.googleapis.com/seu-bucket-aqui/arquivo.m4a"

# Inicia a requisição de transcrição
headers = {
    "authorization": API_KEY,
    "content-type": "application/json"
}
response = requests.post(
    f"{BASE_URL}/transcript",
    json={"audio_url": audio_url, "language_code": "pt"},
    headers=headers
)

transcription_id = response.json()["id"]

# Aguarda até a transcrição ser finalizada
status = "processing"
while status != "completed":
    status_response = requests.get(f"{BASE_URL}/transcript/{transcription_id}", headers=headers)
    status = status_response.json()["status"]
    if status == "error":
        print("Erro na transcrição:", status_response.json()["error"])
        break
    elif status != "completed":
        time.sleep(5)

# Coleta o texto transcrito
text = status_response.json().get("text", "")

# Gera o PDF com o mesmo nome do áudio (sem extensão)
nome_pdf = os.path.basename(audio_url).split(".")[0] + ".pdf"
caminho_pdf = os.path.join("static", nome_pdf)

pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=12)
lines = text.splitlines()
for line in lines:
    pdf.multi_cell(0, 10, line)
pdf.output(caminho_pdf)

print("Transcrição salva em:", caminho_pdf)

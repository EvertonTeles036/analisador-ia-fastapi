from fastapi import FastAPI, Request, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from google.cloud import storage
import os
from typing import List
from datetime import datetime

app = FastAPI()

# Configuração de arquivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

# Nome do bucket no Google Cloud Storage
BUCKET_NAME = "audios-atendimentos-minhaempresa"

# Inicializar cliente do Google Cloud Storage
storage_client = storage.Client()

# Página principal
@app.get("/", response_class=HTMLResponse)
async def form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Rota para upload de 1 arquivo (individual)
@app.post("/upload_single")
async def upload_single_file(file: UploadFile = File(...)):
    # Definindo nome do arquivo com timestamp para evitar conflitos
    blob_name = f"{datetime.now().strftime('%Y%m%d-%H%M%S')}-{file.filename}"
    # Escolhendo o bucket do Cloud Storage
    bucket = storage_client.bucket(BUCKET_NAME)
    blob = bucket.blob(blob_name)
    # Realizando o upload do arquivo
    blob.upload_from_file(file.file, content_type=file.content_type)
    return {"mensagem": f"Arquivo {blob_name} enviado com sucesso."}

# Rota para upload de múltiplos arquivos
@app.post("/upload_multiple")
async def upload_multiple_files(files: List[UploadFile] = File(...)):
    filenames = []
    # Escolhendo o bucket do Cloud Storage
    bucket = storage_client.bucket(BUCKET_NAME)

    for file in files:
        # Definindo nome do arquivo com timestamp para evitar conflitos
        blob_name = f"{datetime.now().strftime('%Y%m%d-%H%M%S')}-{file.filename}"
        # Realizando o upload do arquivo
        blob = bucket.blob(blob_name)
        blob.upload_from_file(file.file, content_type=file.content_type)
        filenames.append(blob_name)

    return {"mensagem": "Arquivos enviados com sucesso.", "arquivos": filenames}

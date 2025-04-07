from fastapi import FastAPI, Request, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from google.cloud import storage
import os
import uuid

app = FastAPI()

# Diretório de arquivos estáticos (CSS, imagens etc.)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Diretório de templates HTML
templates = Jinja2Templates(directory="templates")

# Nome do bucket do Google Cloud Storage
BUCKET_NAME = "audios-atendimentos-minhaempresa"  # Altere para o nome exato do seu bucket

# Página principal com o formulário
@app.get("/", response_class=HTMLResponse)
async def form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Rota para upload individual
@app.post("/upload_single")
async def upload_single(file: UploadFile = File(...)):
    filename = f"{uuid.uuid4()}_{file.filename}"

    client = storage.Client()
    bucket = client.bucket(BUCKET_NAME)
    blob = bucket.blob(filename)
    blob.upload_from_file(file.file, content_type=file.content_type)

    return {"mensagem": "Arquivo enviado com sucesso", "filename": filename}

# Rota para upload múltiplo
@app.post("/upload_multiple")
async def upload_multiple(files: list[UploadFile] = File(...)):
    client = storage.Client()
    bucket = client.bucket(BUCKET_NAME)

    filenames = []
    for file in files:
        filename = f"{uuid.uuid4()}_{file.filename}"
        blob = bucket.blob(filename)
        blob.upload_from_file(file.file, content_type=file.content_type)
        filenames.append(filename)

    return {"mensagem": "Arquivos enviados com sucesso", "filenames": filenames}

from fastapi import FastAPI, Request, UploadFile, File
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from google.cloud import storage
from dotenv import load_dotenv
import os
import uuid

# Carregar variáveis do .env
load_dotenv()

app = FastAPI()

# Diretório de arquivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

# Diretório de templates
templates = Jinja2Templates(directory="templates")

# Nome do bucket do Google Cloud Storage
BUCKET_NAME = os.getenv("GCP_BUCKET_NAME") or "audios-atendimentos-minhaempresa"

# Página principal
@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Upload de um único arquivo
@app.post("/upload_single")
async def upload_single(file: UploadFile = File(...)):
    filename = f"{uuid.uuid4()}_{file.filename}"

    # Validação de tamanho (até 40MB)
    file_size = len(await file.read())
    await file.seek(0)
    if file_size > 40 * 1024 * 1024:
        return JSONResponse(content={"erro": f"O arquivo {file.filename} é muito grande (máx 40MB)"}, status_code=413)

    client = storage.Client()
    bucket = client.bucket(BUCKET_NAME)
    blob = bucket.blob(filename)
    blob.upload_from_file(file.file, content_type=file.content_type)

    return {"mensagem": f"Arquivo {file.filename} enviado com sucesso."}

# Upload de múltiplos arquivos
@app.post("/upload_multiple")
async def upload_multiple(files: list[UploadFile] = File(...)):
    filenames = []
    client = storage.Client()
    bucket = client.bucket(BUCKET_NAME)

    for file in files:
        file_size = len(await file.read())
        await file.seek(0)
        if file_size > 40 * 1024 * 1024:
            return JSONResponse(content={"erro": f"O arquivo {file.filename} é muito grande (máx 40MB)"}, status_code=413)

        filename = f"{uuid.uuid4()}_{file.filename}"
        blob = bucket.blob(filename)
        blob.upload_from_file(file.file, content_type=file.content_type)
        filenames.append(filename)

    return {"mensagem": "Arquivos enviados com sucesso.", "filenames": filenames}


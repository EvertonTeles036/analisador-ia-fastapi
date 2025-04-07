from fastapi import FastAPI, Request, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from google.cloud import storage
import uuid

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

app = FastAPI()

# Middleware global de limite de upload: 100MB
class LimitUploadSizeMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, max_upload_size: int):
        super().__init__(app)
        self.max_upload_size = max_upload_size

    async def dispatch(self, request: Request, call_next):
        content_length = request.headers.get('content-length')
        if content_length and int(content_length) > self.max_upload_size:
            return Response("Arquivo muito grande (limite total: 100MB)", status_code=413)
        return await call_next(request)

app.add_middleware(LimitUploadSizeMiddleware, max_upload_size=100 * 1024 * 1024)

# Diretório de arquivos estáticos (CSS, imagens etc.)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Diretório de templates
templates = Jinja2Templates(directory="templates")

# Nome do bucket do Google Cloud Storage
BUCKET_NAME = "audios-atendimentos-minhaempresa"  # Altere para o seu bucket

# Página principal com o formulário
@app.get("/", response_class=HTMLResponse)
async def form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Rota para upload individual
@app.post("/upload_single")
async def upload_single_file(file: UploadFile = File(...)):
    filename = f"{uuid.uuid4()}_{file.filename}"

    if file.size and file.size > 10 * 1024 * 1024:
        return {"erro": f"O arquivo {file.filename} é muito grande (máx 10MB)"}

    client = storage.Client()
    bucket = client.bucket(BUCKET_NAME)
    blob = bucket.blob(filename)
    blob.upload_from_file(file.file, content_type=file.content_type)

    return {"mensagem": f"Arquivo {filename} enviado com sucesso."}

# Rota para upload múltiplo
@app.post("/upload_multiple")
async def upload_multiple_files(files: list[UploadFile] = File(...)):
    filenames = []
    client = storage.Client()
    bucket = client.bucket(BUCKET_NAME)

    for file in files:
        if file.size and file.size > 10 * 1024 * 1024:
            return {"erro": f"O arquivo {file.filename} é muito grande (máx 10MB)"}
        filename = f"{uuid.uuid4()}_{file.filename}"
        blob = bucket.blob(filename)
        blob.upload_from_file(file.file, content_type=file.content_type)
        filenames.append(filename)

    return {"mensagem": "Arquivos enviados com sucesso.", "filenames": filenames}

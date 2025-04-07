from fastapi import FastAPI, Request, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from google.cloud import storage
import uuid

app = FastAPI()

# Diretório de arquivos estáticos (CSS, imagens etc.)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Diretório de templates HTML
templates = Jinja2Templates(directory="templates")

# Nome do bucket do Google Cloud Storage
BUCKET_NAME = 'audios-atendimentos-minhaempresa'  # Altere para o nome exato do seu bucket

# Página principal que renderiza o formulário
@app.get("/", response_class=HTMLResponse)
async def form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Rota para upload individual
@app.post("/upload_single")
async def upload_single(file: UploadFile = File(...)):
    # Verificando o tamanho do arquivo (limite de 10MB, por exemplo)
    if file.size > 10 * 1024 * 1024:  # 10MB
        return {"message": "O arquivo é muito grande, máximo permitido é 10MB"}
    
    client = storage.Client()
    bucket = client.bucket(BUCKET_NAME)
    blob = bucket.blob(file.filename)
    blob.upload_from_file(file.file, content_type=file.content_type)
    
    return {"message": f"Arquivo {file.filename} enviado com sucesso."}

# Rota para upload múltiplo
@app.post("/upload_multiple")
async def upload_multiple(files: list[UploadFile] = File(...)):
    # Verificando se algum arquivo é maior que 10MB
    for file in files:
        if file.size > 10 * 1024 * 1024:  # 10MB
            return {"message": f"O arquivo {file.filename} é muito grande, máximo permitido é 10MB"}
    
    filenames = []
    client = storage.Client()
    bucket = client.bucket(BUCKET_NAME)
    
    for file in files:
        file_filename = str(uuid.uuid4()) + "-" + file.filename  # Gerando nome único para o arquivo
        blob = bucket.blob(file_filename)
        blob.upload_from_file(file.file, content_type=file.content_type)
        filenames.append(file_filename)
    
    return {"message": "Arquivos enviados com sucesso", "filenames": filenames}

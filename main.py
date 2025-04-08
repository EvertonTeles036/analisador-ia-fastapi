import os
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from google.cloud import storage
from datetime import datetime
from dotenv import load_dotenv

# Carregar variáveis locais (usado apenas em testes locais)
load_dotenv()

# Carregar variáveis do ambiente do container (Cloud Run)
BUCKET_NAME = os.getenv("BUCKET_NAME")
print(f"DEBUG: Bucket definido como: {BUCKET_NAME}")

app = FastAPI()

# Permitir CORS (origens cruzadas)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Página HTML simples
@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <h2>Upload de Áudio para Transcrição com GCS</h2>
    <form action="/upload" method="post" enctype="multipart/form-data">
        <input type="file" name="file" accept="audio/*" required>
        <button type="submit">Enviar para o GCS</button>
    </form>
    """

# Upload de um único arquivo
@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    try:
        print(f"DEBUG: Iniciando upload do arquivo: {file.filename}")
        contents = await file.read()
        filename = datetime.now().strftime("%Y%m%d%H%M%S") + "-" + file.filename
        print(f"DEBUG: Nome final do arquivo gerado: {filename}")

        client = storage.Client()
        print("DEBUG: Cliente GCS criado")

        bucket = client.bucket(BUCKET_NAME)
        print(f"DEBUG: Bucket acessado: {bucket.name}")

        blob = bucket.blob(filename)
        blob.upload_from_string(contents, content_type=file.content_type)
        print("DEBUG: Upload realizado com sucesso!")

        return {
            "mensagem": "Upload realizado com sucesso!",
            "arquivo": filename
        }

    except Exception as e:
        print(f"ERRO: Falha no upload - {str(e)}")
        return JSONResponse(content={"erro": f"Erro no upload para o GCS: {str(e)}"}, status_code=500)

# Geração de URL assinada (GET temporário)
@app.get("/gerar_signed_url")
def gerar_signed_url(filename: str):
    try:
        print(f"DEBUG: Solicitada URL assinada para: {filename}")

        client = storage.Client()
        bucket = client.bucket(BUCKET_NAME)
        blob = bucket.blob(filename)

        url = blob.generate_signed_url(
            version="v4",
            expiration=3600,
            method="GET"
        )
        print(f"DEBUG: URL assinada gerada com sucesso: {url}")

        return {"signed_url": url}

    except Exception as e:
        print(f"ERRO: Falha ao gerar URL - {str(e)}")
        return JSONResponse(content={"erro": f"Erro ao gerar URL assinada: {str(e)}"}, status_code=500)

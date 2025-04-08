import os
from fastapi import FastAPI, Request, UploadFile, File, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from google.cloud import storage
from datetime import timedelta
from pathlib import Path

# Carregar variáveis do .env
load_dotenv()

app = FastAPI()

# CORS para frontend funcionar corretamente
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Caminho dos templates e arquivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

# Página inicial (HTML com upload)
@app.get("/", response_class=HTMLResponse)
async def form():
    return """
    <html>
        <head><title>Upload de Áudio para Transcrição com GCS</title></head>
        <body>
            <h2>Upload de Áudio para Transcrição com GCS</h2>
            <form id="uploadForm" enctype="multipart/form-data">
                <input name="file" type="file"/>
                <button type="button" onclick="uploadFile()">Enviar para o GCS</button>
            </form>
            <div id="status"></div>
            <script>
                async function uploadFile() {
                    const input = document.querySelector('input[type="file"]');
                    const file = input.files[0];
                    if (!file) return;

                    const response = await fetch(`/gerar_signed_url?filename=${file.name}`);
                    const data = await response.json();
                    if (!data.url) {
                        document.getElementById("status").innerText = "Erro ao obter URL assinada.";
                        return;
                    }

                    const upload = await fetch(data.url, {
                        method: "PUT",
                        headers: {
                            "Content-Type": file.type
                        },
                        body: file
                    });

                    if (upload.ok) {
                        document.getElementById("status").innerText = "Upload concluído com sucesso!";
                    } else {
                        document.getElementById("status").innerText = "Erro no envio para o GCS.";
                    }
                }
            </script>
        </body>
    </html>
    """

# NOVA ROTA adicionada: Geração de Signed URL
@app.get("/gerar_signed_url")
def gerar_signed_url(filename: str):
    try:
        print(f"[DEBUG] Rota /gerar_signed_url chamada com filename: {filename}")

        bucket_name = os.getenv("BUCKET_NAME")
        if not bucket_name:
            return JSONResponse(status_code=500, content={"error": "BUCKET_NAME não configurado"})

        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(filename)

        url = blob.generate_signed_url(
            version="v4",
            expiration=timedelta(minutes=10),
            method="PUT",
            content_type="application/octet-stream"
        )

        print(f"[DEBUG] URL assinada gerada: {url}")
        return {"url": url}

    except Exception as e:
        print(f"[ERRO] Falha ao gerar URL assinada: {e}")
        return JSONResponse(status_code=500, content={"error": str(e)})
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from google.cloud import storage
from datetime import timedelta
import os

app = FastAPI()

# Nome do bucket vindo da variável de ambiente
BUCKET_NAME = os.environ.get("BUCKET_NAME")

@app.get("/gerar_signed_url")
async def gerar_signed_url(filename: str):
    try:
        storage_client = storage.Client()
        bucket = storage_client.bucket(BUCKET_NAME)
        blob = bucket.blob(filename)

        url = blob.generate_signed_url(
            version="v4",
            expiration=timedelta(minutes=15),
            method="PUT",
            content_type="application/octet-stream"
        )

        return {"url": url}

    except Exception as e:
        return JSONResponse(status_code=500, content={"erro": str(e)})

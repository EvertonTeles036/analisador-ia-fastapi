import os
from fastapi import FastAPI, Request, UploadFile, File, Form, Query
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

# CORS para permitir acesso do frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Montar arquivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

# Página inicial com formulário de upload
@app.get("/", response_class=HTMLResponse)
async def form():
    return """
    <html>
    <head><title>Upload de Áudio para Transcrição com GCS</title></head>
    <body>
        <h2>Upload de Áudio para Transcrição com GCS</h2>
        <form id="uploadform" enctype="multipart/form-data">
            <input name="file" type="file">
            <button type="button" onclick="uploadFile()">Enviar para o GCS</button>
        </form>
        <div id="status"></div>
        <script>
            async function uploadFile() {
                const input = document.querySelector('input[type="file"]');
                const file = input.files[0];
                if (!file) return;

                document.getElementById('status').innerText = 'Solicitando URL segura...';

                const response = await fetch('/gerar_signed_url?filename=' + file.name);
                const data = await response.json();

                if (data.url) {
                    const upload = await fetch(data.url, {
                        method: 'PUT',
                        headers: {
                            'Content-Type': file.type
                        },
                        body: file
                    });

                    if (upload.ok) {
                        document.getElementById('status').innerText = 'Upload concluído com sucesso!';
                    } else {
                        document.getElementById('status').innerText = 'Erro no envio para o GCS.';
                    }
                } else {
                    document.getElementById('status').innerText = 'Erro ao obter URL assinada.';
                }
            }
        </script>
    </body>
    </html>
    """

# ROTA FINAL — Geração da signed URL
@app.get("/gerar_signed_url")
async def gerar_signed_url(filename: str = Query(...)):
    try:
        BUCKET_NAME = "audios-atendimentos-minhaempresa"  # Substitua pelo seu bucket
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
        print(f"[ERRO] Falha ao gerar URL assinada: {e}")
        return JSONResponse(status_code=500, content={"error": str(e)})

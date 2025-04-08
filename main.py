from fastapi import FastAPI, Request, UploadFile, File
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from google.cloud import storage
from google.oauth2 import service_account
import os
import datetime

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Monta os arquivos estáticos (como index.html)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Define nome do bucket
BUCKET_NAME = "audios-atendimentos-minhaempresa"  # Nome correto do bucket

# Carrega credenciais da conta de serviço
credentials = service_account.Credentials.from_service_account_file(
    "credenciais.json"
)
storage_client = storage.Client(credentials=credentials)

@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <html>
        <head>
            <title>Upload de Áudio para Transcrição com GCS</title>
        </head>
        <body>
            <h2>Upload de Áudio para Transcrição com GCS</h2>
            <form id="upload-form" enctype="multipart/form-data">
                <input type="file" name="file" id="file" />
                <button type="submit">Enviar para o GCS</button>
            </form>
            <div id="progress-bar" style="width: 100%; background-color: #ddd;">
                <div id="progress" style="width: 0%; height: 20px; background-color: red;"></div>
            </div>
            <p id="status"></p>
            <script>
                const form = document.getElementById("upload-form");
                form.addEventListener("submit", async (e) => {
                    e.preventDefault();
                    const fileInput = document.getElementById("file");
                    const file = fileInput.files[0];
                    if (!file) {
                        document.getElementById("status").innerText = "Selecione um arquivo.";
                        return;
                    }

                    const response = await fetch(`/gerar_signed_url?filename=${file.name}`);
                    if (!response.ok) {
                        document.getElementById("status").innerText = "Erro ao gerar URL.";
                        return;
                    }

                    const data = await response.json();
                    const signedUrl = data.url;
                    const upload = await fetch(signedUrl, {
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
                });
            </script>
        </body>
    </html>
    """

@app.get("/gerar_signed_url")
async def gerar_signed_url(filename: str):
    try:
        bucket = storage_client.bucket(BUCKET_NAME)
        blob = bucket.blob(filename)

        url = blob.generate_signed_url(
            version="v4",
            expiration=datetime.timedelta(minutes=15),
            method="PUT",
            content_type="application/octet-stream"
        )

        return JSONResponse(content={"url": url})
    except Exception as e:
        return JSONResponse(content={"erro": str(e)}, status_code=500)

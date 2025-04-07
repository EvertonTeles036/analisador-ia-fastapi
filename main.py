import os
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse
from google.cloud import storage
from datetime import datetime

app = FastAPI()

# Caminho fixo da chave de autenticação (ajuste se necessário)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/seu-usuario/nome-da-chave.json"

# Nome do bucket fixo
BUCKET_NAME = "audios-atendimentos-minhaempresa"

@app.get("/", response_class=HTMLResponse)
async def index():
    return """
    <html>
        <head>
            <title>Upload de Áudio</title>
        </head>
        <body>
            <h1>Upload de Áudio para Transcrição com GCS</h1>
            <form action="/upload" enctype="multipart/form-data" method="post">
                <input name="file" type="file">
                <input type="submit" value="Enviar para o GCS">
            </form>
        </body>
    </html>
    """

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    try:
        contents = await file.read()

        # Criação do nome único para o arquivo
        now = datetime.utcnow().strftime("%Y%m%d-%H%M%S")
        filename = f"{now}-{file.filename}"

        # Inicialização do cliente GCS
        client = storage.Client()
        bucket = client.bucket(BUCKET_NAME)
        blob = bucket.blob(filename)

        # Upload do conteúdo
        blob.upload_from_string(contents, content_type=file.content_type)

        return {"mensagem": "Upload realizado com sucesso!", "arquivo": filename}

    except Exception as e:
        return {"erro": str(e)}

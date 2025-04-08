import os
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse
from google.cloud import storage
from datetime import datetime

app = FastAPI()

# Nome do bucket
BUCKET_NAME = "audios-atendimentos-minhaempresa"

@app.get("/", response_class=HTMLResponse)
def form():
    return """
    <html>
        <head>
            <title>Upload de Áudio para Transcrição com GCS</title>
        </head>
        <body>
            <h3>Upload de Áudio para Transcrição com GCS</h3>
            <form action="/upload/" enctype="multipart/form-data" method="post">
                <input name="file" type="file">
                <input type="submit" value="Enviar para o GCS">
            </form>
        </body>
    </html>
    """

@app.post("/upload/")
async def upload(file: UploadFile = File(...)):
    try:
        # Lê o conteúdo do arquivo enviado
        contents = await file.read()

        # Gera um nome único baseado na data e hora
        now = datetime.utcnow().strftime("%Y%m%d-%H%M%S")
        filename = f"{now}_{file.filename}"

        # Inicializa o cliente do Google Cloud Storage
        client = storage.Client()
        bucket = client.bucket(BUCKET_NAME)
        blob = bucket.blob(filename)

        # Faz o upload para o GCS
        blob.upload_from_string(contents, content_type=file.content_type)

        return {
            "message": "Upload realizado com sucesso!",
            "arquivo": filename
        }

    except Exception as e:
        return {
            "erro": f"Erro no upload para o GCS: {str(e)}"
        }

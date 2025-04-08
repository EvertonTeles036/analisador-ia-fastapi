import os
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse, JSONResponse
from google.cloud import storage
from datetime import datetime, timedelta

app = FastAPI()

# Nome do bucket
BUCKET_NAME = "audios-atendimentos-minhaempresa"

@app.get("/")
def form():
    content = """
    <html>
        <head>
            <title>Upload de Áudio para Transcrição com GCS</title>
        </head>
        <body>
            <h1>Upload de Áudio para Transcrição com GCS</h1>
            <form action="/upload" enctype="multipart/form-data" method="post">
                <input type="file" name="file">
                <input type="submit" value="Enviar para o GCS">
            </form>
        </body>
    </html>
    """
    return HTMLResponse(content=content)

@app.post("/upload")
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

        # Faz upload para o GCS
        blob.upload_from_string(contents, content_type=file.content_type)

        return { "message": "Upload realizado com sucesso!", "arquivo": filename }
    except Exception as e:
        return { "erro": f"Erro no upload para o GCS: {str(e)}" }

# Rota para gerar URL assinada para upload direto no GCS
@app.get("/gerar_signed_url")
async def gerar_signed_url(filename: str):
    try:
        client = storage.Client()
        bucket = client.bucket(BUCKET_NAME)
        blob = bucket.blob(filename)

        url = blob.generate_signed_url(
            version="v4",
            expiration=timedelta(minutes=15),
            method="PUT",
            content_type="audio/m4a",
        )

        return JSONResponse(content={"url": url})
    except Exception as e:
        return JSONResponse(content={"erro": str(e)}, status_code=500)

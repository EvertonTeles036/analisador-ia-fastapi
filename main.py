import os
from fastapi import FastAPI, UploadFile, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from google.cloud import storage
from dotenv import load_dotenv
from datetime import timedelta
import requests

# Carrega variáveis de ambiente
load_dotenv()

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

BUCKET_NAME = os.getenv("BUCKET_NAME")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/gerar_signed_url")
async def gerar_signed_url(filename: str):
    print(f"DEBUG: Rota acionada para gerar signed URL do arquivo: {filename}")
    bucket_name = os.getenv("BUCKET_NAME")
    print(f"DEBUG: Bucket name: {bucket_name}")

    if not bucket_name:
        return JSONResponse(status_code=500, content={"message": "BUCKET_NAME não configurado"})

    try:
        client = storage.Client()
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(filename)

        url = blob.generate_signed_url(
            version="v4",
            expiration=timedelta(minutes=15),
            method="PUT",
            content_type="application/octet-stream"
        )

        print(f"DEBUG: URL assinada gerada: {url}")
        return {"url": url}
    except Exception as e:
        print(f"ERRO ao gerar signed URL: {str(e)}")
        return JSONResponse(status_code=500, content={"message": f"Erro ao gerar signed URL: {str(e)}"})

@app.post("/upload/")
async def upload_file(file: UploadFile):
    try:
        contents = await file.read()
        filename = file.filename
        bucket_name = BUCKET_NAME

        print(f"DEBUG: Iniciando upload para bucket {bucket_name} com arquivo {filename}")
        client = storage.Client()
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(filename)
        blob.upload_from_string(contents)

        print(f"DEBUG: Upload concluído: {filename}")
        return {"message": f"Arquivo {filename} enviado com sucesso para o bucket {bucket_name}!"}
    except Exception as e:
        print(f"ERRO no upload: {str(e)}")
        return {"message": f"Erro ao fazer upload: {str(e)}"}

@app.post("/enviar_formulario")
async def enviar_formulario(nome: str = Form(...), email: str = Form(...)):
    print(f"Formulário recebido - Nome: {nome}, Email: {email}")
    return {"message": "Formulário recebido com sucesso", "nome": nome, "email": email}

@app.get("/teste")
async def teste():
    return {"status": "ok"}

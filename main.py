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
        <form id="uploadform" enctype="multipart/form-data">
            <input name="file" type="file">
            <button type="button" onclick="uploadFile()">Enviar para o GCS</button>
        </


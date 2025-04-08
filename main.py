import os
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse
from google.cloud import storage
from dotenv import load_dotenv
from datetime import datetime

# Carrega as variáveis do arquivo .env
load_dotenv()

# Inicializa o app
app = FastAPI()

# Pega o nome do bucket do .env
BUCKET_NAME = os.getenv("BUCKET_NAME")

@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <h2>Upload de Áudio para Transcrição com GCS</h2>
    <input type="file" id="fileInput" accept="audio/*" />
    <br>
    <button onclick="enviarParaGCS()">Enviar para o GCS</button>
    <div id="status"></div>
    <script>
        async function enviarParaGCS() {
            const fileInput = document.getElementById("fileInput");
            const statusDiv = document.getElementById("status");

            if (!fileInput.files.length) {
                statusDiv.innerText = "Selecione um arquivo.";
                return;
            }

            const file = fileInput.files[0];
            const formData = new FormData();
            formData.append("file", file);

            statusDiv.innerText = "Enviando...";

            const response = await fetch("/upload", {
                method: "POST",
                body: formData
            });

            const result = await response.json();
            statusDiv.innerText = result.message;
        }
    </script>
    """

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{file.filename}"

        client = storage.Client()
        bucket = client.bucket(BUCKET_NAME)
        blob = bucket.blob(filename)
        blob.upload_from_string(contents, content_type=file.content_type)

        return {
            "message": f"Upload realizado com sucesso para {BUCKET_NAME}/{filename}",
            "filename": filename
        }

    except Exception as e:
        return {"message": f"Erro ao enviar para o GCS: {str(e)}"}

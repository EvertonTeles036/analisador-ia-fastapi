from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
import os

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("formulario.html", {"request": request})

@app.post("/transcrever")
async def transcrever(file: UploadFile = File(...)):
    nome = file.filename.rsplit(".", 1)[0]
    caminho_pdf = f"{nome}.pdf"
    with open(caminho_pdf, "w") as f:
        f.write(f"Transcrição simulada para o áudio: {file.filename}")
    return FileResponse(caminho_pdf, media_type="application/pdf", filename=caminho_pdf)
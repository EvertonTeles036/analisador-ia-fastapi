from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("formulario.html", {"request": request})

@app.post("/transcrever")
async def transcrever_audio(file: UploadFile = File(...)):
    conteudo = await file.read()
    if not conteudo:
        return JSONResponse(content={"erro": "Arquivo vazio"}, status_code=400)
    return JSONResponse(content={"transcricao": "Transcrição simulada do áudio recebido"})

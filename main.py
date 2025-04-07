from fastapi import FastAPI, Request, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import List

app = FastAPI()

# Arquivos estáticos (CSS, imagens, etc)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates HTML
templates = Jinja2Templates(directory="templates")

# Rota principal que renderiza o formulário HTML
@app.get("/", response_class=HTMLResponse)
async def render_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Rota para upload de um único áudio
@app.post("/upload_single")
async def upload_single(file: UploadFile = File(...)):
    return {"filename": file.filename}

# Rota para upload múltiplo de áudios
@app.post("/upload_multiple")
async def upload_multiple(files: List[UploadFile] = File(...)):
    filenames = [file.filename for file in files]
    return {"filenames": filenames}

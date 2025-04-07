from fastapi import FastAPI, Request, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import List

app = FastAPI()

# Arquivos estáticos (CSS, imagens etc.)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

# Página principal
@app.get("/", response_class=HTMLResponse)
async def form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Rota de upload individual
@app.post("/upload_single")
async def upload_single(file: UploadFile = File(...)):
    return {"filename": file.filename}

# Rota de upload múltiplo
@app.post("/upload_multiple")
async def upload_multiple(files: List[UploadFile] = File(...)):
    filenames = [file.filename for file in files]
    return {"filenames": filenames}

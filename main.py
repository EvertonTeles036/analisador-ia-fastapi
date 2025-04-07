from fastapi import FastAPI, Request, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

# Diretório de arquivos estáticos (CSS, imagens etc.)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Diretório de templates HTML
templates = Jinja2Templates(directory="templates")

# Rota principal que renderiza o formulário
@app.get("/", response_class=HTMLResponse)
async def form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Rota POST que recebe o upload de áudio
@app.post("/upload_single")
async def upload_audio(file: UploadFile = File(...)):
    return {"filename": file.filename}

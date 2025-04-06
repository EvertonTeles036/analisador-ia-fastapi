from fastapi import FastAPI, UploadFile, File
from transcriber import processar_audio
from fastapi.responses import FileResponse

app = FastAPI()

@app.get("/")
def home():
    return {"mensagem": "API com AssemblyAI e divisão de áudio ativa."}

@app.post("/transcrever")
async def transcrever(file: UploadFile = File(...)):
    pdf_path = await processar_audio(file)
    return FileResponse(pdf_path, media_type='application/pdf', filename=pdf_path.split('/')[-1])
from fastapi import FastAPI, UploadFile, File
from transcriber import transcribe_audio

app = FastAPI()

@app.get("/")
def home():
    return {"mensagem": "API de Análise de Áudio rodando com sucesso"}

@app.post("/transcrever")
async def transcrever_audio(file: UploadFile = File(...)):
    resultado = await transcribe_audio(file)
    return {"transcricao": resultado}

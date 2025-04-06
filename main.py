from fastapi import FastAPI, UploadFile, File
from transcriber import transcrever_audio
from analyzer import analisar_texto
from reporter import gerar_relatorio

app = FastAPI()

@app.get("/")
def read_root():
    return {"mensagem": "API de Análise de Áudio rodando com sucesso!"}

@app.post("/transcrever")
async def transcrever(file: UploadFile = File(...)):
    audio_bytes = await file.read()
    resultado = transcrever_audio(audio_bytes)
    return resultado

@app.post("/analisar")
def analisar(payload: dict):
    texto = payload.get("texto", "")
    resultado = analisar_texto(texto)
    return resultado

@app.post("/relatorio")
def relatorio(payload: dict):
    dados = payload.get("dados", {})
    resultado = gerar_relatorio(dados)
    return resultado
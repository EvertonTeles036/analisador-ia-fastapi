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
    return await transcrever_audio(file)

@app.post("/analisar")
def analisar(texto: str):
    return analisar_texto(texto)

@app.post("/relatorio")
def relatorio(texto: str):
    return gerar_relatorio(texto)
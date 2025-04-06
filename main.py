
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
from transcriber import transcrever_arquivos
from analyzer import analisar_texto
from reporter import gerar_relatorio
import shutil
import os

app = FastAPI()

@app.get("/")
async def root():
    return {"mensagem": "API de Análise de Áudio rodando com sucesso!"}

@app.post("/transcrever")
async def transcrever_endpoint(arquivos: list[UploadFile] = File(...)):
    resultados = transcrever_arquivos(arquivos)
    return JSONResponse(content=resultados)

@app.post("/analisar")
async def analisar_endpoint(texto: str = Form(...)):
    resultado = analisar_texto(texto)
    return JSONResponse(content=resultado)

@app.post("/relatorio")
async def relatorio_endpoint(texto: str = Form(...)):
    resultado = gerar_relatorio(texto)
    return JSONResponse(content=resultado)

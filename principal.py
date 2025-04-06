
from fastapi import FastAPI, UploadFile, File
import os
from transcritor import converter_audio_generico, transcrever_audio
from analisador import analisar_texto
from reporter import gerar_relatorio

app = FastAPI()

@app.get("/")
def home():
    return {"mensagem": "API de Análise de Áudio rodando com sucesso!"}

@app.post("/transcrever-avancado")
async def transcrever_avancado(file: UploadFile = File(...)):
    extensao = file.filename.split(".")[-1]
    caminho_temp = f"temp_entrada.{extensao}"
    with open(caminho_temp, "wb") as f:
        f.write(await file.read())

    caminho_convertido = converter_audio_generico(caminho_temp)
    transcricao = transcrever_audio(caminho_convertido)
    resultado_analise = analisar_texto(transcricao)
    relatorio = gerar_relatorio(transcricao, resultado_analise)

    os.remove(caminho_temp)
    os.remove(caminho_convertido)

    return {
        "transcricao": transcricao,
        "analise": resultado_analise,
        "relatorio": relatorio
    }


from fastapi import FastAPI, UploadFile, File
from transcriber import transcribe_audio
from analisador import analisar_texto
from reporter import gerar_relatorio

app = FastAPI()

@app.get("/")
def home():
    return {"mensagem": "API de Análise de Áudio rodando com sucesso!"}

@app.post("/transcrever-avancado")
async def transcrever_avancado(file: UploadFile = File(...)):
    # Utiliza o utilitário de transcrição assíncrono
    transcricao = await transcribe_audio(file)
    resultado_analise = analisar_texto(transcricao)
    relatorio = gerar_relatorio(transcricao)

    return {
        "transcricao": transcricao,
        "analise": resultado_analise,
        "relatorio": relatorio
    }

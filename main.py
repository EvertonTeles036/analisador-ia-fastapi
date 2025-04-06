from fastapi import FastAPI, Request
from analisador import analyze_transcription

app = FastAPI()

@app.post("/analisar/")
async def analisar(request: Request):
    body = await request.json()
    texto = body.get("texto", "")
    resultado = analyze_transcription(texto)
    return resultado

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"mensagem": "API de Análise de Áudio rodando com sucesso"}

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"mensagem": "API de Análise de Áudio rodando com sucesso"}
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]

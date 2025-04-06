from fastapi import FastAPI
import uvicorn
import os

aplicativo = FastAPI()

@aplicativo.get("/")
def ler_raiz():
    return {"mensagem": "API FastAPI rodando com sucesso no Cloud Run!"}

if __name__ == "__main__":
    porta = int(os.environ.get("PORT", 8080))
    uvicorn.run("principal:aplicativo", host="0.0.0.0", port=porta)

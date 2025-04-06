from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"mensagem": "API FastAPI rodando com sucesso no Cloud Run!"}

@app.post("/analisar")
def analisar_texto(texto: str):
    if "obrigado" in texto.lower():
        return {"sentimento": "positivo"}
    elif "ruim" in texto.lower():
        return {"sentimento": "negativo"}
    else:
        return {"sentimento": "neutro"}

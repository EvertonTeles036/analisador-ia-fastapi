# FastAPI main app entry point
from fastapi import FastAPI
app = FastAPI()

@app.get('/')
def read_root():
    return {'mensagem': 'API de Análise de Áudio rodando com sucesso'}
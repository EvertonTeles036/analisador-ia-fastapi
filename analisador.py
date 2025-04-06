def analisar_texto(texto):
    if not texto:
        return {"erro": "Texto vazio"}
    return {"resposta": f"Análise feita com sucesso para: {texto}"}
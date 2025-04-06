from transformers import pipeline

def analisar_texto(texto):
    if not texto:
        return {"erro": "Texto vazio"}

    sentiment_pipeline = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")
    resultado = sentiment_pipeline(texto)
    return {"sentimento": resultado}
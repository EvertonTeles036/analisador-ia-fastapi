from datetime import datetime
import json
import os

def gerar_relatorio(dados, pasta="relatorios"):
    if not os.path.exists(pasta):
        os.makedirs(pasta)
    nome_arquivo = f"{pasta}/relatorio_{datetime.now().strftime('%Y%m%d%H%M%S')}.json"
    with open(nome_arquivo, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)
    return nome_arquivo

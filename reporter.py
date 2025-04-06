
def gerar_relatorio(transcricao, analise):
    return f"""
RELATÓRIO DE ATENDIMENTO

Transcrição:
{transcricao}

Análise:
- Pontos positivos: {', '.join(analise['pontos_positivos'])}
- Pontos de melhoria: {', '.join(analise['pontos_melhoria'])}
- Emoção predominante: {analise['emocao_predominante']}
- Nota: {analise['nota']}
Justificativa: {analise['justificativa']}
"""

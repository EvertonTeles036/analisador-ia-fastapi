# Analisador de Atendimentos com IA

Este projeto é uma API desenvolvida em FastAPI para análise de atendimentos via gravações de áudio, utilizando inteligência artificial para transcrição, interpretação e geração de relatórios em PDF com insights personalizados.

## Funcionalidades

- Upload de arquivos de áudio (.mp3 ou .wav)
- Transcrição automática com AssemblyAI
- Análise crítica com ChatGPT (OpenAI)
- Geração de relatório final em PDF
- Deploy escalável no Google Cloud Run

## Tecnologias Utilizadas

- FastAPI
- Uvicorn
- AssemblyAI
- OpenAI (ChatGPT)
- ReportLab
- Google Cloud Run
- GitHub Actions (Deploy automático)
- Python 3.12+

## Como Usar Localmente

```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio
pip install -r requisitos.txt --user
uvicorn main:app --reload --host 0.0.0.0 --port 8080
```

Depois, acesse `http://localhost:8080` e envie um POST para `/analisar/` com um áudio (.mp3/.wav).

## Variáveis de Ambiente Necessárias

As seguintes variáveis devem ser adicionadas no Cloud Run ou em um arquivo `.env`:

- `ASSEMBLYAI_API_KEY`
- `OPENAI_API_KEY`
- `SECRET_KEY`

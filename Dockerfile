FROM python:3.10-slim

# Variável de ambiente para desativar o buffer do Python (log imediato)
ENV PYTHONUNBUFFERED=1

# Instala dependências do sistema
RUN apt-get update && apt-get install -y gcc libffi-dev

# Define diretório de trabalho
WORKDIR /app

# Copia os arquivos para dentro do container
COPY . /app

# Instala as bibliotecas do projeto
RUN pip install --no-cache-dir -r requirements.txt

# Comando para rodar o app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]

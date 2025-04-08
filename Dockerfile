FROM python:3.11-slim

# Desativa o buffer do Python para logs em tempo real
ENV PYTHONUNBUFFERED=1

# Instala dependências do sistema (inclui suporte a libffi, útil para algumas libs como cryptography)
RUN apt-get update && apt-get install -y gcc libffi-dev

# Cria diretório de trabalho
WORKDIR /app

# Copia todos os arquivos do projeto, incluindo o .env
COPY . .

# Instala bibliotecas
RUN pip install --no-cache-dir -r requirements.txt

# Comando para rodar o servidor
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]

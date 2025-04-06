FROM python:3.10

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requisitos.txt

CMD ["uvicorn", "principal:aplicativo", "--host", "0.0.0.0", "--port", "8080"]


FROM python:3.10

WORKDIR /app

COPY . /app

RUN apt-get update && apt-get install -y ffmpeg
RUN pip install --no-cache-dir -r requisitos.txt

CMD ["uvicorn", "principal:app", "--host", "0.0.0.0", "--port", "8080"]

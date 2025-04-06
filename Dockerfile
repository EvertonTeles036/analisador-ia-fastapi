FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
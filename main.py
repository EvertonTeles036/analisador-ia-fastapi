from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/")
def read_root():
    return {"mensagem": "API no ar e funcionando com FastAPI no Cloud Run"}

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8080))  # pega a porta do Cloud Run
    uvicorn.run("principal:app", host="0.0.0.0", port=port, reload=False)

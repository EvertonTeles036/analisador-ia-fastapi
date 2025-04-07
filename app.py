
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", response_class=HTMLResponse)
async def read_form():
    with open("index.html", "r", encoding="utf-8") as file:
        return HTMLResponse(content=file.read())

@app.post("/upload_single")
async def upload_single(file: UploadFile = File(...)):
    return {"status": "success", "filename": file.filename}

@app.post("/upload_multiple")
async def upload_multiple(files: List[UploadFile] = File(...)):
    return {"status": "success", "filenames": [file.filename for file in files]}

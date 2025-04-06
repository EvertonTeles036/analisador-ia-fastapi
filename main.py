from fastapi import FastAPI, UploadFile, File
from transcriber import transcribe_audio
from analyzer import analyze_transcription
from reporter import generate_report

app = FastAPI()

@app.post("/analisar/")
async def analisar_audio(file: UploadFile = File(...)):
    content = await file.read()
    transcription = transcribe_audio(content)
    analise = analyze_transcription(transcription)
    pdf_path = generate_report(transcription, analise)
    return {"mensagem": "Relatório gerado", "arquivo_pdf": pdf_path}
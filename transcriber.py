import os
import tempfile
import ffmpeg
import whisper
from fastapi import UploadFile

SUPPORTED_FORMATS = [".mp3", ".mp4", ".m4a", ".mov", ".webm", ".3gp"]

async def transcrever_audio(file: UploadFile):
    ext = os.path.splitext(file.filename)[-1].lower()
    if ext not in SUPPORTED_FORMATS:
        return {"erro": "Formato de áudio não suportado"}

    with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
        tmp.write(await file.read())
        input_path = tmp.name

    output_path = input_path + ".mp3"
    ffmpeg.input(input_path).output(output_path).run(overwrite_output=True)

    model = whisper.load_model("base")
    result = model.transcribe(output_path, language="pt")

    os.remove(input_path)
    os.remove(output_path)

    return {"transcricao": result["text"]}
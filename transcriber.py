import os
from dotenv import load_dotenv
import assemblyai as aai

load_dotenv()
API_KEY = os.getenv("ASSEMBLYAI_API_KEY")
if not API_KEY:
    raise ValueError("ASSEMBLYAI_API_KEY não definido nas variáveis de ambiente")

aai.settings.api_key = API_KEY

async def transcribe_audio(file):
    path = f"temp_{file.filename}"
    with open(path, "wb") as f:
        f.write(await file.read())

    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(path)

    os.remove(path)
    return transcript.text if transcript else "Erro na transcrição"

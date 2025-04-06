import os
import assemblyai as aai

aai.settings.api_key = "d7f4166d1399467a95aac2d8ef4e8421"

async def transcribe_audio(file):
    path = f"temp_{file.filename}"
    with open(path, "wb") as f:
        f.write(await file.read())

    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(path)

    os.remove(path)
    return transcript.text if transcript else "Erro na transcrição"

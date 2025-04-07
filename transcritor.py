
import requests
import time
import os

ASSEMBLYAI_API_KEY = os.getenv("ASSEMBLYAI_API_KEY")

def transcribe_from_gcs(gcs_url):
    headers = {
        "authorization": ASSEMBLYAI_API_KEY,
        "content-type": "application/json"
    }
    json = {
        "audio_url": gcs_url,
        "auto_chapters": False
    }
    response = requests.post("https://api.assemblyai.com/v2/transcript", json=json, headers=headers)
    transcript_id = response.json()["id"]

    while True:
        polling_response = requests.get(f"https://api.assemblyai.com/v2/transcript/{transcript_id}", headers=headers)
        status = polling_response.json()["status"]
        if status == "completed":
            return polling_response.json()["text"]
        elif status == "error":
            return f"Erro: {polling_response.json()['error']}"
        time.sleep(5)

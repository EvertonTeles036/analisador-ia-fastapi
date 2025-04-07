
import base64
import json
import subprocess

def pubsub_trigger(event, context):
    if 'data' in event:
        data = base64.b64decode(event['data']).decode('utf-8')
        message = json.loads(data)
        audio_url = message.get('audio_url')
        if audio_url:
            subprocess.run(["python3", "transcritor.py", audio_url])

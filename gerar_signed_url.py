
from fastapi import FastAPI
from google.cloud import storage
from datetime import timedelta
import os

app = FastAPI()

@app.get("/generate-signed-url/")
def generate_signed_url(filename: str):
    storage_client = storage.Client()
    bucket_name = os.environ.get("GCS_BUCKET_NAME")
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(filename)

    url = blob.generate_signed_url(
        version="v4",
        expiration=timedelta(minutes=15),
        method="PUT",
        content_type="application/octet-stream",
    )

    return {"upload_url": url}

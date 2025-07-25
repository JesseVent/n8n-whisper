from fastapi import FastAPI, File, UploadFile, Header, HTTPException, Query
from faster_whisper import WhisperModel
import tempfile
import os

app = FastAPI()

# Load the smallest model
model = WhisperModel("tiny")

# Set your API token here (you can load it from env vars in production)
API_TOKEN = os.getenv("WHISPER_API_TOKEN", "changeme123")

@app.post("/transcribe")
async def transcribe(
    file: UploadFile = File(...),
    authorization: str = Header(None),
    language: str = Query(default=None, description="Language spoken in the audio (e.g., 'en', 'th')"),
    translate: bool = Query(default=False, description="Whether to translate output to English"),
):
    # Token-based authentication
    if not authorization or authorization != f"Bearer {API_TOKEN}":
        raise HTTPException(status_code=401, detail="Invalid or missing token")

    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=file.filename) as tmp:
        contents = await file.read()
        tmp.write(contents)
        tmp_path = tmp.name

    segments, info = model.transcribe(
        tmp_path,
        beam_size=5,
        language=language,
        task="translate" if translate else "transcribe"
    )

    transcript = "".join([segment.text for segment in segments])
    return {
        "transcript": transcript,
        "language": info.language,
        "duration": info.duration
    }

from fastapi import Request
import requests

@app.post("/transcribe-url")
async def transcribe_url(
    request: Request,
    authorization: str = Header(None),
    language: str = Query(default=None, description="Language spoken in the audio (e.g., 'en', 'th')"),
    translate: bool = Query(default=False, description="Whether to translate output to English"),
):
    if not authorization or authorization != f"Bearer {API_TOKEN}":
        raise HTTPException(status_code=401, detail="Invalid or missing token")

    body = await request.json()
    audio_url = body.get("url")
    if not audio_url:
        raise HTTPException(status_code=400, detail="Missing 'url' in request body")

    # Download the audio file
    response = requests.get(audio_url)
    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Failed to download audio file")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".audio") as tmp:
        tmp.write(response.content)
        tmp_path = tmp.name

    segments, info = model.transcribe(
        tmp_path,
        beam_size=5,
        language=language,
        task="translate" if translate else "transcribe"
    )

    transcript = "".join([segment.text for segment in segments])
    return {
        "transcript": transcript,
        "language": info.language,
        "duration": info.duration,
        "source_url": audio_url
    }

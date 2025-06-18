# Logic for calling Whisper API

"""
    Purpose:
    Sends the uploaded audio file to OpenAI Whisper API
    Returns the raw transcription text
"""


import requests
import time
import os
import aiohttp
import os
from fastapi import UploadFile
from dotenv import load_dotenv

load_dotenv()

# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ASSEMBLYAI_API_KEY = os.getenv("ASSEMBLYAI_API_KEY")
BASE_URL = "https://api.assemblyai.com"

headers = {
    "authorization": ASSEMBLYAI_API_KEY
}

async def transcribe_audio(audio: UploadFile) -> str:
    # Save uploaded file temporarily
    temp_path = f"/tmp/{audio.filename}"
    with open(temp_path, "wb") as f:
        f.write(await audio.read())

    # Upload to AssemblyAI
    with open(temp_path, "rb") as f:
        upload_response = requests.post(f"{BASE_URL}/v2/upload", headers=headers, data=f)
    audio_url = upload_response.json()["upload_url"]

    # Submit for transcription
    data = {
        "audio_url": audio_url,
        "speech_model": "universal"
    }
    transcript_response = requests.post(f"{BASE_URL}/v2/transcript", json=data, headers=headers)
    transcript_id = transcript_response.json()["id"]

    # Polling until completion
    polling_url = f"{BASE_URL}/v2/transcript/{transcript_id}"
    while True:
        result = requests.get(polling_url, headers=headers).json()
        if result['status'] == 'completed':
            return result['text']
        elif result['status'] == 'error':
            raise RuntimeError(f"Transcription failed: {result['error']}")
        time.sleep(3)
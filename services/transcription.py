# Logic for calling Whisper API

"""
    Purpose:
    Sends the uploaded audio file to OpenAI Whisper API
    Returns the raw transcription text
"""


import aiohttp
import os
from fastapi import UploadFile
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

async def transcribe_audio(audio: UploadFile) -> str:
    url = "https://api.openai.com/v1/audio/transcriptions"

    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }

    data = aiohttp.FormData()
    data.add_field("file", await audio.read(), filename="meeting.webm", content_type="audio/webm")
    data.add_field("model", "whisper-1")

    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=data, headers=headers) as response:
            if response.status != 200:
                error = await response.text()
                raise Exception(f"Whisper API failed: {error}")

            result = await response.json()
            return result["text"]

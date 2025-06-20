# summarizer.py
import os
from dotenv import load_dotenv
import google.generativeai as genai
import asyncio

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Choose the model: fast and good enough for summarizing
model = genai.GenerativeModel("models/gemini-2.5-flash")

async def summarize_text(transcript: str) -> str:
#     prompt = f"""
# You are a meeting assistant. Summarize the following meeting transcript in a professional tone. Highlight:

# - Key discussion points
# - Decisions made
# - Action items (if any)

# Transcript:
# \"\"\"
# {transcript}
# \"\"\"
# """
    prompt = f"""
You are a helpful assistant. Summarize the following text clearly and concisely:

\"\"\"
{transcript}
\"\"\"
"""


    loop = asyncio.get_event_loop()
    response = await loop.run_in_executor(None, model.generate_content, prompt)

    return response.text.strip()

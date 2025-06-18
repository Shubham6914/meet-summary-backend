# GPT summarization logic


"""
    Purpose:
    Takes the transcript text and generates a:

    Short summary of the meeting

    List of action items (if applicable)
"""



import openai
import os
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

async def summarize_text(transcript: str) -> str:
    prompt = f"""
You are a meeting assistant. Summarize the following meeting transcript in a professional tone. Highlight:

- Key discussion points
- Decisions made
- Action items (if any)

Transcript:
\"\"\"
{transcript}
\"\"\"
"""

    response = await openai.ChatCompletion.acreate(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes meeting notes."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.5,
        max_tokens=600
    )

    summary = response.choices[0].message.content.strip()
    return summary

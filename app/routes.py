# Route for handling rotes of apps

"""This file defines the main route:
        POST /submit-audio/ — it:

        Accepts audio + email data from the extension

        Calls the transcription and summarization logic

        Sends the final summary to the given email addresses
"""
from fastapi import APIRouter, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse
from services.transcription import transcribe_audio
from services.summarizer import summarize_text
from utils.emailer import send_summary_email

router = APIRouter()

@router.post("/submit-audio/")
async def submit_audio(
    audio: UploadFile,
    your_email: str = Form(...),
    participant_emails: str = Form("")  # comma-separated
):
    try:
        # Step 1: Transcribe the audio
        transcript = await transcribe_audio(audio)

        # Step 2: Summarize the transcript using GPT
        summary = await summarize_text(transcript)

        # Step 3: Combine all emails
        all_emails = [your_email] + [
            email.strip() for email in participant_emails.split(",") if email.strip()
        ]

        # Step 4: Send email to all participants
        await send_summary_email(to_emails=all_emails, summary_text=summary)

        return JSONResponse({"message": " Meeting summary sent to participants."})

    except Exception as e:
        print(" Error:", e)
        raise HTTPException(status_code=500, detail="Something went wrong.")

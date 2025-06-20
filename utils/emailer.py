# Logic to send summary emails

import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

print("SMTP_USER:", SMTP_USER)
print("SMTP_PASSWORD:", SMTP_PASSWORD)


async def send_summary_email(to_emails: list, summary_text: str):
    subject = "📝 Meeting Summary"
    
    # Create email content
    html_content = f"""
    <html>
        <body>
            <h2>Meeting Summary</h2>
            <p>{summary_text.replace('\n', '<br>')}</p>
            <p>Regards,<br><b>Meet Summary AI</b></p>
        </body>
    </html>
    """

    for email in to_emails:
        message = MIMEMultipart()
        message["From"] = SMTP_USER
        message["To"] = email
        message["Subject"] = subject

        message.attach(MIMEText(html_content, "html"))

        try:
            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                server.starttls()
                server.login(SMTP_USER, SMTP_PASSWORD)
                server.send_message(message)
                print(f" Summary sent to {email}")
        except Exception as e:
            print(f"Failed to send email to {email}: {e}")

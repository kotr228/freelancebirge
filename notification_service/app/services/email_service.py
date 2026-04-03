import os
import aiosmtplib
from email.message import EmailMessage

async def send_email_task(to_email: str, subject: str, body: str):
    if not to_email:
        return
    
    msg = EmailMessage()
    msg["From"] = os.getenv("SMTP_USER", "noreply@freelance.birge")
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.set_content(body)

    try:
        await aiosmtplib.send(
            msg,
            hostname=os.getenv("SMTP_HOST", "smtp.gmail.com"),
            port=int(os.getenv("SMTP_PORT", 465)),
            use_tls=True,
            username=os.getenv("SMTP_USER"),
            password=os.getenv("SMTP_PASS"),
        )
        print(f"📧 Email sent to {to_email}")
    except Exception as e:
        print(f"❌ Email error: {e}")
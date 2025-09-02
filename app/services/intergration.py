import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.utils.config import GMAIL_APP_PASSWORD

async def send_email_gmail(receiver_email: str, subject: str, body: str):
    try:
        sender_email = "jan.lvvarshney@gmail.com"
        app_password = GMAIL_APP_PASSWORD

        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = receiver_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, app_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()

        return {"status": "sent", "channel": "email", "to": receiver_email}
    except Exception as e:
        return {"status": "failed", "channel": "email", "error": str(e)}

from fastapi import FastAPI, Request
from fastapi import APIRouter, Query
from pydantic import BaseModel
from typing import Optional, Dict
from app.services.intergration import send_email_gmail

router = APIRouter(prefix="/notify", tags=["Notification"])


class SMSMessage(BaseModel):
    text: str

class NotificationMessage(BaseModel):
    title: str
    body: str

class EmailMessage(BaseModel):
    subject: str
    body: str

class MessageRequest(BaseModel):
    email: Optional[EmailMessage] = None
    sms: Optional[SMSMessage] = None
    notification: Optional[NotificationMessage] = None
    user_email: Optional[str] = None
    user_phone_number: Optional[str] = None

async def send_email(content: str, user_email):
    email_RESP = await send_email_gmail(user_email, content.subject, content.body)
    print(f"[EMAIL SENT] {email_RESP}")
    return {"status": "sent", "channel": "email"}

def send_sms(content: str):
    print(f"[SMS SENT] {content['text']}")
    return {"status": "sent", "channel": "sms"}

def send_notification(content: Dict[str, str]):
    print(f"[NOTIFICATION SENT] Title: {content['title']}, Body: {content['body']}")
    return {"status": "sent", "channel": "notification"}

@router.post("/send-message")
async def send_message(message: MessageRequest):
    response = {}

    if message.email:
        response["email"] = await send_email(message.email, message.user_email)

    if message.sms:
        response["sms"] = send_sms(message.sms.dict(), message.user_phone_number)

    if message.notification:
        response["notification"] = send_notification(message.notification.dict())

    return {
        "status": "completed",
        "results": response
    }

# app/services/notification_service.py

import requests

class NotificationService:
    def __init__(self):
        self.email_api_url = "https://example.com/send-email"
        self.sms_api_url = "https://example.com/send-sms"

    def send_email(self, to: str, subject: str, message: str):
        print(f"📧 Sending Email to {to} | {subject}: {message}")
        return {"status": "success", "to": to, "channel": "email"}

    def send_sms(self, to: str, message: str):
        # Dummy logic (replace with Twilio, Gupshup, etc.)
        print(f"📱 Sending SMS to {to}: {message}")
        return {"status": "success", "to": to, "channel": "sms"}

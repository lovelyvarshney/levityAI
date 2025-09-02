import requests
import os
from app.utils.config import OPENAI_API_KEY

OPENAI_URL = "https://api.openai.com/v1/chat/completions"

def _get_prompt(delay: int, channel: str) -> str:
    """
    Build a channel-specific prompt based on delay severity.
    """
    if 10 <= delay <= 20:
        tone = "a short, friendly, and reassuring"
    elif 30 <= delay <= 60:
        tone = "a detailed, empathetic, and reassuring"
    else:
        tone = "a highly empathetic, professional, and proactive"

    if channel == "email":
        return (
            f"The delivery is delayed by {delay} minutes. "
            f"Write {tone} email with a clear subject and body. "
            "Format response strictly as:\n"
            '{"subject": "...", "body": "..."}'
        )
    elif channel == "sms":
        return (
            f"The delivery is delayed by {delay} minutes. "
            f"Write {tone} SMS text in under 160 characters. "
            "Make it concise and include a placeholder [tracking_link]. "
            "Format response strictly as:\n"
            '{"text": "..."}'
        )
    elif channel == "notification":
        return (
            f"The delivery is delayed by {delay} minutes. "
            f"Write {tone} mobile app notification. "
            "Provide both title and body. "
            "Format response strictly as:\n"
            '{"title": "...", "body": "..."}'
        )
    return ""


def _call_openai(prompt: str) -> dict:
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }

    body = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant for delivery updates. Always return valid JSON strictly in the requested format."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 200,
        "temperature": 0.7
    }

    response = requests.post(OPENAI_URL, headers=headers, json=body)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"].strip()


def generate_delay_messages(delay: int, channels: dict) -> dict:
    messages = {}

    for channel, value in channels.items():
        if not value:
            continue

        prompt = _get_prompt(delay, channel)

        try:
            raw = _call_openai(prompt)

            # Try parsing JSON output from AI
            import json
            parsed = json.loads(raw)

            messages[channel] = parsed

        except Exception as e:
            print(f"AI fallback for {channel}: {e}")
            if channel == "email":
                messages[channel] = {
                    "subject": f"Delivery Update – Delay of {delay} mins",
                    "body": f"Dear Customer,\n\nYour delivery is delayed by {delay} minutes. "
                            "We’re working hard to get it to you quickly. "
                            "Thank you for your patience.\n\n– Team"
                }
            elif channel == "sms":
                messages[channel] = {
                    "text": f"Hi! Your delivery is delayed by {delay} mins. Track here: [tracking_link]. Thanks for your patience!"
                }
            elif channel == "notification":
                messages[channel] = {
                    "title": "Delivery Update",
                    "body": f"Your order is delayed by {delay} mins. We’ll notify you once it’s closer."
                }

    return messages
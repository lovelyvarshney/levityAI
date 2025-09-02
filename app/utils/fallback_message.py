FALLBACK_MESSAGE = (
    "Your delivery is experiencing delays. "
    "We sincerely apologize for the inconvenience and assure you we are working to resolve it as soon as possible."
)

FALLBACK_MESSAGES = {
    "sms": (
        "Your delivery is delayed. We’re sorry for the inconvenience. "
        "Our team is working to resolve it quickly."
    ),
    "email": ({
        "subject": "Delivery update: Your package is delayed.",
        "body": "Dear Customer,\n\n"
            "We regret to inform you that your delivery is currently experiencing delays. "
            "We sincerely apologize for the inconvenience and want to assure you that our team is working hard to resolve the issue as soon as possible.\n\n"
            "Thank you for your patience.\n\n"
            "Best regards,\nDelivery Support Team"
    }),
    "notification": ({
        "heading": "Delivery update: Your package is delayed.",
        "body": "We’re working to fix this and will notify you soon."
    }),
}

def get_fallback_message(channel: str) -> str:
    return FALLBACK_MESSAGES.get(channel, FALLBACK_MESSAGE)

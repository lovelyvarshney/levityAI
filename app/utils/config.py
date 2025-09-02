import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")
NOTIFICATION_API_KEY = os.getenv("NOTIFICATION_API_KEY")
GMAIL_APP_PASSWORD= os.getenv("GMAIL_APP_PASSWORD")
MAX_ALLOWED_DELAY = 30
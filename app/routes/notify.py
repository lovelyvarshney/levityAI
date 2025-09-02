import os
from fastapi import APIRouter, Query
from app.services.traffic_service import get_route_delay
from app.services.ai_service import generate_delay_messages
from app.services.ai_evaluation_service import evaluate_message
from app.utils.validators import NotifyRequest
from app.utils.response import build_customer_messages
from app.services.intergration import send_email_gmail

FALLBACK_MESSAGE = "Your delivery is experiencing delays. We sincerely apologize for the inconvenience and assure you we are working to resolve it as soon as possible."

router = APIRouter(prefix="/notify", tags=["Notification"])

@router.post("/customer")
async def notify_customer(payload: NotifyRequest):

    data = payload.dict()
    origin = data.get("origin", "")
    destination = data.get("destination", "")

    traffic_data = await get_route_delay(origin, destination, data.get("mock_data", False))
    print("traffic_data ", traffic_data)
    delay = traffic_data["delay"]

    max_delay_allowed = data.get("custom_max_delay_allowed") or 30
    print("max_delay_allowed" , max_delay_allowed)
    if delay <= max_delay_allowed:
        return {
            "status": "no_delay",
            "message": f"Delay is only {delay} minutes. No notification needed."
        }

    channels = data.get("channels", {"notification" : True})
    print("channels ", channels)
    ai_message = generate_delay_messages(delay, channels)
    print("ai_message ::: ", ai_message)
    channel_score = evaluate_message(ai_message)
    print("channel_score ", channel_score)

    _response =  build_customer_messages(channels, channel_score, ai_message, data, delay)

    _email_data = _response.get("customer_messages", {}).get("email")
    await send_email_gmail(data.get("channels").get("email", None) , _email_data.get("subject"), _response.get("body"))
    return _response
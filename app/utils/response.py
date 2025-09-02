from app.utils.fallback_message import get_fallback_message

def build_customer_messages(channels, channel_score, ai_message, data, delay):
    customer_messages = {}
    for channel, value in channels.items():
        if not value:
            continue

        score = channel_score.get(channel, 0)

        if score >= 4:
            if isinstance(ai_message, dict):
                customer_messages[channel] = ai_message.get(channel)
            else:
                customer_messages[channel] = ai_message
        else:
            fallback_msg = (
                data.get("fallback_message", {}).get(channel, {}).get("notification")
            )

            print("fallback_msg ::: ", fallback_msg)

            if fallback_msg:
                customer_messages[channel] = fallback_msg
            else:
                customer_messages[channel] = get_fallback_message(channel)

    return {
        "status": "multi-channel",
        "delay": delay,
        "scores": channel_score,
        "customer_messages": customer_messages,
    }


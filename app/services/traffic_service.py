import random
import requests
import os
import re

def _normalize_location(value: str) -> str:
    value = value.strip()

    if value.startswith("place_id:"):
        return value

    coord_pattern = re.compile(r"^-?\d+(\.\d+)?,-?\d+(\.\d+)?$")
    if coord_pattern.match(value):
        return value

    return value.replace(" ", "+")

async def get_route_delay(origin: str, destination: str, mock_response: bool = False) -> dict:
    """
    Get route delay either as a mock response or via actual API call.
    Supports origin/destination as addresses, coordinates, or place_ids.
    """

    origin = _normalize_location(origin)
    destination = _normalize_location(destination)

    if mock_response:
        print("true")
        normal_duration = 45
        current_duration = random.randint(45, 120)
        delay = current_duration - normal_duration

        return {
            "origin": origin,
            "destination": destination,
            "normal_duration": normal_duration,
            "current_duration": current_duration,
            "delay": delay
        }

    else:
        api_key = os.getenv("GOOGLE_MAPS_API_KEY")
        if not api_key:
            raise ValueError("Missing GOOGLE_MAPS_API_KEY in environment variables")

        url = (
            f"https://maps.googleapis.com/maps/api/distancematrix/json"
            f"?origins={origin}&destinations={destination}&departure_time=now&key={api_key}"
        )

        print("URL ", url)
        response = requests.get(url)
        data = response.json()

        if "rows" not in data or not data["rows"]:
            raise ValueError("Invalid response from Google Maps API")

        element = data["rows"][0]["elements"][0]

        normal_duration = element.get("duration", {}).get("value", 0) // 60
        current_duration = element.get("duration_in_traffic", {}).get("value", normal_duration * 60) // 60
        delay = current_duration - normal_duration

        return {
            "origin": origin,
            "destination": destination,
            "normal_duration": normal_duration,
            "current_duration": current_duration,
            "delay": delay
        }

import requests
import json

def get_weather(city=None):
    """Fetch live weather and temperature for a specified city or auto-detected location."""
    if not city or city.lower().strip() in ["here", "my location", "current location", "today"]:
        location = ""
    else:
        location = city.strip()

    try:
        url = f"https://wttr.in/{location}?format=j1"
        res = requests.get(url, timeout=5)
        if res.status_code == 200:
            data = res.json()
            curr = data["current_condition"][0]
            temp_c = curr["temp_C"]
            desc = curr["weatherDesc"][0]["value"].strip()
            humidity = curr["humidity"]
            feels = curr["FeelsLikeC"]

            city_name = location.capitalize() if location else "your location"
            return (
                f"The current weather in {city_name} is {desc} with a temperature of {temp_c} degrees Celsius. "
                f"It feels like {feels} degrees Celsius with {humidity} percent humidity, Boss!"
            )
    except Exception:
        pass

    return "Could not fetch weather data right now. Please check your internet connection."

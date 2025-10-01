import requests       # For making HTTP requests to the weather API
import logging        # For logging warnings and debug information

from modules.unit_conversion import kmh_to_mph, to_24_hour_clock # Converts kilometers per hour to miles per hour & set to 24 clock

def fetch_weather(api_url):
    """
    Fetches weather data from the specified API URL.
    Returns a formatted weather summary string and a list of the next 5 forecast entries.
    """
    try:
        response = requests.get(api_url, timeout=5)		# Send GET request to the weather API with a timeout of 5 seconds
        data = response.json()
        weather = data.get("weather", {})
        forecast = data.get("forecast_next", [])[:5]	# Extract the next 5 forecast entries
        wind_kmh = weather.get("wind_speed_kmh", "")
        wind_txt = kmh_to_mph(wind_kmh)
        # Format a readable weather summary string
        weather_text = f"{weather.get('temperature_celsius', 'N/A')}C, {weather.get('condition', 'N/A')}, {wind_txt}, {weather.get('humidity_percent', 'N/A')}% Hum"
        sun_data = data.get("sunrise_sunset", {})
        sunrise = to_24_hour_clock(sun_data.get("sunrise", "N/A"))
        sunset = to_24_hour_clock(sun_data.get("sunset", "N/A"))

        return weather_text, forecast, sunrise, sunset	# Return the summary and forecast list

    except Exception as e:
        logging.warning(f"Weather fetch failed: {e}") 	# Log a warning if the request or parsing fails
        return "Weather unavailable", []				# Return fallback values

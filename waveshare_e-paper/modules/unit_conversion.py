from datetime import datetime

def kmh_to_mph(kmh, round_result=True, fallback_unit="km/h"):
    """
    Converts kilometers per hour to miles per hour.

    Parameters:
        kmh (float or int): Speed in kilometers per hour.
        round_result (bool): If True, rounds the result to nearest integer.
        fallback_unit (str): Unit to use if input is invalid.

    Returns:
        str: Formatted string with mph value or fallback.
    """
    try:
        mph = kmh * 0.621371
        if round_result:
            mph = round(mph)
        return f"{mph} mph"
    except (TypeError, ValueError):
        return f"{kmh} {fallback_unit}"

def to_24_hour_clock(time_str):
    """
    Converts a 12-hour time string (e.g., '6:58:27 AM') to 24-hour format (e.g., '06:58').

    Parameters:
        time_str (str): Time string in 12-hour format.

    Returns:
        str: Time string in 24-hour format (HH:MM), or original if conversion fails.
    """
    try:
        dt = datetime.strptime(time_str, "%I:%M:%S %p")
        return dt.strftime("%H:%M")
    except (ValueError, TypeError):
        return time_str  # fallback if input is invalid
        

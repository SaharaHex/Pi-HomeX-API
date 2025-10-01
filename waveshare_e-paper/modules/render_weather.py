from PIL import ImageDraw  # Provides drawing capabilities for PIL images
from modules.unit_conversion import kmh_to_mph # Converts kilometers per hour to miles per hour.

def draw_weather_center(draw, epd, text, font):
    """
    Draws the main weather summary text centered horizontally and slightly above vertical center.
    
    Parameters:
        draw (ImageDraw.Draw): Drawing context for the black image layer.
        epd (EPD): The e-paper display object, used to get screen dimensions.
        text (str): The weather summary string to display.
        font (ImageFont): Font used to render the weather text.
    
    Returns:
        int: The Y-coordinate just below the weather text, used to position forecast boxes.
    """
    # Measure the bounding box of the weather text
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    # Calculate centered position
    x = (epd.width - text_width) // 2
    y = (epd.height // 2) - text_height // 2 - 30  # Slightly above center

    # Draw the weather text
    draw.text((x, y), text, font=font, fill=0)

    # Return the Y-position for the next row of forecast boxes
    return y + text_height + 20


def draw_forecast_boxes(drawblack, drawry, epd, forecast, start_y, font):
    """
    Draws 5 horizontal forecast boxes below the weather summary.
    
    Parameters:
        drawblack (ImageDraw.Draw): Drawing context for black layer (text).
        drawry (ImageDraw.Draw): Drawing context for red/yellow layer (box outlines).
        epd (EPD): The e-paper display object, used to get screen dimensions.
        forecast (list): List of forecast entries (dicts) to display.
        start_y (int): Y-coordinate to begin drawing the boxes.
        font (ImageFont): Font used for forecast text.
    """
    left_margin = 15
    right_margin = 15
    box_spacing = 5
    usable_width = epd.width - left_margin - right_margin
    box_width = (usable_width - (box_spacing * 4)) // 5  # Divide screen into 5 equal boxes
    box_height = 115              						 # Fixed height for each forecast box
    corner_radius = 8              						 # Radius for rounded corners

    for i, entry in enumerate(forecast):
        box_x = left_margin + i * (box_width + box_spacing)

        # Draw the box outline on the red/yellow layer
        drawry.rounded_rectangle(
            (box_x, start_y, box_x + box_width, start_y + box_height),
            radius=corner_radius,
            outline=0
        )

        # Extract and format forecast details
        time_txt = entry.get("time", "")
        temp_txt = f"{entry.get('temperature_celsius', '')} C"
        cond_txt = entry.get("condition", "")[:12]  # Truncate condition to fit
        wind_kmh = entry.get("wind_speed_kmh", "")
        wind_txt = kmh_to_mph(wind_kmh)
        hum_txt = f"{entry.get('humidity_percent', '')} % humidity"

        # Draw forecast text inside the box on the black layer
        drawblack.text((box_x + 10, start_y + 5), time_txt, font=font, fill=0)
        drawblack.text((box_x + 10, start_y + 25), temp_txt, font=font, fill=0)
        drawblack.text((box_x + 10, start_y + 45), cond_txt, font=font, fill=0)
        drawblack.text((box_x + 10, start_y + 65), wind_txt, font=font, fill=0)
        drawblack.text((box_x + 10, start_y + 85), hum_txt, font=font, fill=0)

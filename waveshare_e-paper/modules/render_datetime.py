from PIL import ImageFont
import datetime

def draw_datetime_top_left(draw, epd, font_path):
    """
    Draws UK-formatted date and 24-hour time in the top-left corner.

    Parameters:
        draw (ImageDraw.Draw): Drawing context for the black layer.
        epd (EPD): E-paper display object for screen dimensions.
        font_path (str): Path to the font file.
    """
    # Get current local time
    now = datetime.datetime.now()

    # Format date and time
    date_str = now.strftime("%A, %d %b %Y")   # e.g., Thursday 25 Sep 2025
    time_str = now.strftime("Last Updated, %H:%M")         # 24-hour format

    # Load font
    try:
        font = ImageFont.truetype(font_path, 20)
    except IOError:
        font = ImageFont.load_default() 

    # Position text with padding
    x = 13
    y_date = 13
    y_time = y_date + 24  # space below date

    # Draw both lines
    draw.text((x, y_date), date_str, font=font, fill=0)
    draw.text((x, y_time), time_str, font=font, fill=0)
    

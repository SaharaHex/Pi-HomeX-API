from PIL import ImageFont, ImageDraw

def draw_sunrise_sunset(drawblack, drawry, epd, sunrise, sunset, font_path):
    """
    Draws sunrise and sunset times in two boxes in the top-right corner.

    Parameters:
        drawblack (ImageDraw.Draw): Drawing context for black layer.
        drawry (ImageDraw.Draw): Drawing context for red/yellow layer.
        epd (EPD): E-paper display object.
        sunrise (str): Sunrise time string.
        sunset (str): Sunset time string.
        font_path (str): Path to the font file.
    """
    try:
        font = ImageFont.truetype(font_path, 20)
    except IOError:
        font = ImageFont.load_default()

    box_width = 140
    box_height = 30
    right_margin = 13
    top_margin = 13
    spacing = 8

    box_x = epd.width - box_width - right_margin

    # Sunrise box
    sunrise_y = top_margin
    drawry.rectangle((box_x, sunrise_y, box_x + box_width, sunrise_y + box_height), outline=0)
    text_sunrise_y = sunrise_y + (box_height - font.getsize(f"Sunrise {sunrise}")[1])
    drawblack.text((box_x + 8, text_sunrise_y), f"Sunrise {sunrise}", font=font, fill=0)

    # Sunset box
    sunset_y = sunrise_y + box_height + spacing
    drawry.rectangle((box_x, sunset_y, box_x + box_width, sunset_y + box_height), outline=0)
    text_sunset_y = sunset_y + (box_height - font.getsize(f"Sunset {sunset}")[1])
    drawblack.text((box_x + 8, text_sunset_y), f"Sunset {sunset}", font=font, fill=0)

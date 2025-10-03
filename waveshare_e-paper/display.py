# This retrieves weather data from a local API running on a Raspberry Pi and displays it on a 792×272 E-paper display.
import sys, os, time, logging

# Define paths to 'pic' and 'lib' directories relative to this script
picdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pic')
libdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib')

# Add 'lib' to Python's module search path if it exists
if os.path.exists(libdir): 
    sys.path.append(libdir)

# External libraries
from PIL import ImageFont                         # For loading custom fonts
from waveshare_epd import epd5in79b               # E-paper display driver

# Custom modules
from modules.weather_api import fetch_weather       # Fetches weather data from API
from modules.render_sun import draw_sunrise_sunset  # Drawing functions for sunrise & sunset
from modules.render_weather import draw_weather_center, draw_forecast_boxes  # Drawing functions weather
from modules.render_datetime import draw_datetime_top_left # Drawing functions for date & time
from modules.epd_setup import initialize_display    # Initializes display and drawing surfaces
from modules.logging_setup import setup_logging     # Configures logging to either console or a log file.

# For console output during development
#setup_logging(to_console=True, level=logging.DEBUG)

# For crontab-safe file logging
setup_logging(to_console=False)

def main():
    logging.info("weather display")

    # Initialize the e-paper display
    epd = epd5in79b.EPD()
    HBlackimage, HRYimage, drawblack, drawry = initialize_display(epd)

    # Fetch weather summary and next 5 forecast entries
    weather_text, forecast, sunrise, sunset = fetch_weather("http://Your Ip address:3000/weather")

    # Load fonts from 'pic' directory
    font_large = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 36)
    font_small = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 20)

    # Draw centered weather summary and get Y-position for forecast boxes
    forecast_y = draw_weather_center(drawblack, epd, weather_text, font_large)

    # Draw 5 horizontal forecast boxes below the weather summary
    draw_forecast_boxes(drawblack, drawry, epd, forecast, forecast_y, font_small)
    
    # Draws sunrise and sunset times in the top-right corner of the display
    draw_sunrise_sunset(drawblack, drawry, epd, sunrise, sunset, os.path.join(picdir, 'Font.ttc'))
    
    # Draws UK-formatted date and 24-hour time in the top-left corner
    draw_datetime_top_left(drawblack, epd, os.path.join(picdir, 'Font.ttc'))

    # Rotate images 180 to match physical screen orientation
    HBlackimage = HBlackimage.rotate(180)
    HRYimage = HRYimage.rotate(180)

    # Send the images to the display
    epd.display(epd.getbuffer(HBlackimage), epd.getbuffer(HRYimage))
    time.sleep(2)

if __name__ == "__main__":
    try:
        main()
    except IOError as e:
        logging.info(e)
    except KeyboardInterrupt:
        logging.info("ctrl + c:")
        epd5in79b.epdconfig.module_exit(cleanup=True)
        exit()

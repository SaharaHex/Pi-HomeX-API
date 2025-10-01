from PIL import Image, ImageDraw  # Used to create and draw on image buffers for the e-paper display

def initialize_display(epd):
    """
    Initializes the e-paper display and prepares drawing surfaces.
    
    Parameters:
        epd (EPD): The e-paper display object.
    
    Returns:
        tuple: A set of initialized image buffers and drawing contexts:
            - HBlackimage: Monochrome image for black layer
            - HRYimage: Monochrome image for red/yellow layer
            - drawblack: Drawing context for black layer
            - drawry: Drawing context for red/yellow layer
    """
    # Initialize and clear the e-paper display hardware
    epd.init()
    epd.Clear()

    # Create blank white images for both black and red/yellow layers
    HBlackimage = Image.new('1', (epd.width, epd.height), 255)  # '1' mode = 1-bit pixels, 255 = white
    HRYimage = Image.new('1', (epd.width, epd.height), 255)

    # Create drawing contexts for each image layer
    drawblack = ImageDraw.Draw(HBlackimage)
    drawry = ImageDraw.Draw(HRYimage)

    # Draw a border rectangle on the red/yellow layer
    drawry.rectangle((10, 10, epd.width - 10, epd.height - 10), outline=0)

    # Return all image buffers and drawing contexts
    return HBlackimage, HRYimage, drawblack, drawry
    

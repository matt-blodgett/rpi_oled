import board
import busio
import adafruit_ssd1306

from PIL import Image
from PIL import ImageDraw

from .constants import DISPLAY_WIDTH
from .constants import DISPLAY_HEIGHT


class Display:

    def __init__(self):
        i2c = busio.I2C(board.SCL, board.SDA)
        self._display = adafruit_ssd1306.SSD1306_I2C(DISPLAY_WIDTH, DISPLAY_HEIGHT, i2c)
        self.clear()

    def set_image(self, image):
        self._display.image(image)
        self._display.show()

    def clear(self):
        self._display.fill(0)
        self._display.show()

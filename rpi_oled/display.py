import board
import busio
import adafruit_ssd1306

from PIL import Image
from PIL import ImageDraw


class Display:

    def __init__(self):
        i2c = busio.I2C(board.SCL, board.SDA)
        self.display = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)

        self.display.fill(0)
        self.display.show()

        width = self.display.width
        height = self.display.height
        self.image = Image.new('1', (width, height))

        self.draw = ImageDraw.Draw(self.image)
        self.draw.rectangle((0, 0, width, height), outline=0, fill=0)

    def update(self):
        self.display.image(self.image)
        self.display.show()

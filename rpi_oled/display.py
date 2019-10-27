import board
import busio

import adafruit_ssd1306

from PIL import Image
from PIL import ImageDraw


class Display:

    def __init__(self):
        i2c = busio.I2C(board.SCL, board.SDA)
        disp = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)

        disp.fill(0)
        disp.show()

        width = disp.width
        height = disp.height
        image = Image.new('1', (width, height))

        draw = ImageDraw.Draw(image)
        draw.rectangle((0, 0, width, height), outline=0, fill=0)

        self.draw = draw
        self.disp = disp
        self.image = image

    def update(self):
        self.disp.image(self.image)
        self.disp.show()

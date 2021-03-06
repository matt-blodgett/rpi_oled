import board
import busio
import adafruit_ssd1306

from PIL import Image
from PIL import ImageDraw


class Display:

    def __init__(self):
        i2c = busio.I2C(board.SCL, board.SDA)
        self._display = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)

        self._display.fill(0)
        self._display.show()

        width = self._display.width
        height = self._display.height
        self.image = Image.new('1', (width, height))

        self.draw = ImageDraw.Draw(self.image)
        self.draw.rectangle((0, 0, width, height), outline=0, fill=0)

    def set_image(self, image: Image) -> None:
        self._display.image(image)
        self._display.show()

    def update(self) -> None:
        self._display.image(self.image)
        self._display.show()

    def clear(self) -> None:
        self._display.fill(0)
        self._display.show()

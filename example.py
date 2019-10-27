import board
import busio

import adafruit_ssd1306

from PIL import Image
from PIL import ImageDraw

from rpi_oled.controller import Button
from rpi_oled.controller import Controller


i2c = busio.I2C(board.SCL, board.SDA)
disp = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)


disp.fill(0)
disp.show()

width = disp.width
height = disp.height
image = Image.new('1', (width, height))

draw = ImageDraw.Draw(image)
draw.rectangle((0, 0, width, height), outline=0, fill=0)


keys = Controller()


while True:
    keys.read_state()

    if Button.UP not in keys.pressed:
        draw.polygon([(20, 20), (30, 2), (40, 20)], outline=255, fill=0)
    else:
        draw.polygon([(20, 20), (30, 2), (40, 20)], outline=255, fill=1)

    if Button.LEFT not in keys.pressed:
        draw.polygon([(0, 30), (18, 21), (18, 41)], outline=255, fill=0)
    else:
        draw.polygon([(0, 30), (18, 21), (18, 41)], outline=255, fill=1)

    if Button.RIGHT not in keys.pressed:
        draw.polygon([(60, 30), (42, 21), (42, 41)], outline=255, fill=0)
    else:
        draw.polygon([(60, 30), (42, 21), (42, 41)], outline=255, fill=1)

    if Button.DOWN not in keys.pressed:
        draw.polygon([(30, 60), (40, 42), (20, 42)], outline=255, fill=0)
    else:
        draw.polygon([(30, 60), (40, 42), (20, 42)], outline=255, fill=1)

    if Button.CENTER not in keys.pressed:
        draw.rectangle((20, 22, 40, 40), outline=255, fill=0)
    else:
        draw.rectangle((20, 22, 40, 40), outline=255, fill=1)

    if Button.A not in keys.pressed:
        draw.ellipse((70, 40, 90, 60), outline=255, fill=0)
    else:
        draw.ellipse((70, 40, 90, 60), outline=255, fill=1)

    if Button.B not in keys.pressed:
        draw.ellipse((100, 20, 120, 40), outline=255, fill=0)
    else:
        draw.ellipse((100, 20, 120, 40), outline=255, fill=1)

    disp.image(image)
    disp.show()

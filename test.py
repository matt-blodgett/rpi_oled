from rpi_oled import Controller
from rpi_oled import Button
from rpi_oled import Display


controller = Controller()
display = Display()


try:
    while True:
        controller.update_state()

        if Button.A not in controller.buttons.pressed:
            display.draw.ellipse((70, 40, 90, 60), outline=255, fill=0)
        else:
            display.draw.ellipse((70, 40, 90, 60), outline=255, fill=1)

        if Button.B not in controller.buttons.pressed:
            display.draw.ellipse((100, 20, 120, 40), outline=255, fill=0)
        else:
            display.draw.ellipse((100, 20, 120, 40), outline=255, fill=1)

        if Button.UP not in controller.buttons.pressed:
            display.draw.polygon([(20, 20), (30, 2), (40, 20)], outline=255, fill=0)
        else:
            display.draw.polygon([(20, 20), (30, 2), (40, 20)], outline=255, fill=1)

        if Button.LEFT not in controller.buttons.pressed:
            display.draw.polygon([(0, 30), (18, 21), (18, 41)], outline=255, fill=0)
        else:
            display.draw.polygon([(0, 30), (18, 21), (18, 41)], outline=255, fill=1)

        if Button.RIGHT not in controller.buttons.pressed:
            display.draw.polygon([(60, 30), (42, 21), (42, 41)], outline=255, fill=0)
        else:
            display.draw.polygon([(60, 30), (42, 21), (42, 41)], outline=255, fill=1)

        if Button.DOWN not in controller.buttons.pressed:
            display.draw.polygon([(30, 60), (40, 42), (20, 42)], outline=255, fill=0)
        else:
            display.draw.polygon([(30, 60), (40, 42), (20, 42)], outline=255, fill=1)

        if Button.CENTER not in controller.buttons.pressed:
            display.draw.rectangle((20, 22, 40, 40), outline=255, fill=0)
        else:
            display.draw.rectangle((20, 22, 40, 40), outline=255, fill=1)

        display.update()

        if Button.CENTER in controller.buttons.pressed and Button.A in controller.buttons.pressed:
            display.clear()
            exit(1)

except KeyboardInterrupt:
    display.clear()

exit(1)


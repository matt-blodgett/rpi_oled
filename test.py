from rpi_oled import Controller
from rpi_oled import Button
from rpi_oled import Display


def main():
    controller = Controller()
    display = Display()

    try:
        while True:
            controller.update_buttons_state()

            if controller.is_released(Button.A):
                display.draw.ellipse((100, 20, 120, 40), outline=255, fill=0)
            else:
                display.draw.ellipse((100, 20, 120, 40), outline=255, fill=1)

            if controller.is_released(Button.B):
                display.draw.ellipse((70, 40, 90, 60), outline=255, fill=0)
            else:
                display.draw.ellipse((70, 40, 90, 60), outline=255, fill=1)

            if controller.is_released(Button.UP):
                display.draw.polygon([(20, 20), (30, 2), (40, 20)], outline=255, fill=0)
            else:
                display.draw.polygon([(20, 20), (30, 2), (40, 20)], outline=255, fill=1)

            if controller.is_released(Button.LEFT):
                display.draw.polygon([(0, 30), (18, 21), (18, 41)], outline=255, fill=0)
            else:
                display.draw.polygon([(0, 30), (18, 21), (18, 41)], outline=255, fill=1)

            if controller.is_released(Button.RIGHT):
                display.draw.polygon([(60, 30), (42, 21), (42, 41)], outline=255, fill=0)
            else:
                display.draw.polygon([(60, 30), (42, 21), (42, 41)], outline=255, fill=1)

            if controller.is_released(Button.DOWN):
                display.draw.polygon([(30, 60), (40, 42), (20, 42)], outline=255, fill=0)
            else:
                display.draw.polygon([(30, 60), (40, 42), (20, 42)], outline=255, fill=1)

            if controller.is_released(Button.CENTER):
                display.draw.rectangle((20, 22, 40, 40), outline=255, fill=0)
            else:
                display.draw.rectangle((20, 22, 40, 40), outline=255, fill=1)

            display.update()

            controller.update_buttons_state()
            if controller.is_pressed(Button.CENTER) and controller.is_pressed(Button.A):
                display.clear()
                break

    except KeyboardInterrupt:
        display.clear()
        exit(1)


if __name__ == '__main__':
    main()

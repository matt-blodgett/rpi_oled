from rpi_oled.config import ApplicationConfig
from rpi_oled.state import ApplicationState
from rpi_oled.controller import Controller
from rpi_oled.display import Display
from rpi_oled.constants import Button


def main():
    config = ApplicationConfig()
    state = ApplicationState(config)
    controller = Controller()
    display = Display()

    state.initialize(display.set_image)

    all_buttons = [
        Button.A,
        Button.B,
        Button.UP,
        Button.LEFT,
        Button.RIGHT,
        Button.DOWN,
        Button.CENTER
    ]

    try:
        current_button = None

        while True:
            controller.update()

            if current_button is None:
                for button in all_buttons:
                    if controller.is_pressed(button):
                        current_button = button
                        break
            else:
                if controller.is_released(current_button):
                    state.update(current_button)
                    current_button = None

    except KeyboardInterrupt:
        display.clear()
        exit(1)


if __name__ == '__main__':
    main()

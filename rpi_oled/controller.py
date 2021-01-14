import enum

import board
import digitalio


class Button(enum.Enum):
    A = 'A'
    B = 'B'
    UP = 'U'
    LEFT = 'L'
    RIGHT = 'R'
    DOWN = 'D'
    CENTER = 'M'


class Controller:

    def __init__(self):
        self.buttons_pressed = []
        self.buttons_released = [
            Button.A,
            Button.B,
            Button.UP,
            Button.DOWN,
            Button.LEFT,
            Button.RIGHT,
            Button.CENTER
        ]

        self._button_to_pin_map = {
            Button.A: digitalio.DigitalInOut(board.D6),
            Button.B: digitalio.DigitalInOut(board.D5),
            Button.UP: digitalio.DigitalInOut(board.D17),
            Button.LEFT: digitalio.DigitalInOut(board.D27),
            Button.RIGHT: digitalio.DigitalInOut(board.D23),
            Button.DOWN: digitalio.DigitalInOut(board.D22),
            Button.CENTER: digitalio.DigitalInOut(board.D4)
        }

        for pin in self._button_to_pin_map.values():
            pin.direction = digitalio.Direction.INPUT
            pin.pull = digitalio.Pull.UP

    def update_buttons_state(self) -> None:
        self.buttons_pressed = [button for button, pin in self._button_to_pin_map.items() if not pin.value]
        self.buttons_released = [button for button, pin in self._button_to_pin_map.items() if pin.value]

    def is_pressed(self, button: Button) -> bool:
        return button in self.buttons_pressed

    def is_released(self, button: Button) -> bool:
        return button in self.buttons_released

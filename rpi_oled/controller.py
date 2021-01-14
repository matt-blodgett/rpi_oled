import enum

import board
from digitalio import DigitalInOut
from digitalio import Direction
from digitalio import Pull


class Button(enum.Enum):
    A = 'A'
    B = 'B'
    UP = 'U'
    LEFT = 'L'
    RIGHT = 'R'
    DOWN = 'D'
    CENTER = 'M'


class ButtonStates:

    def __init__(self):
        self.pressed = []
        self.released = [
            Button.A,
            Button.B,
            Button.UP,
            Button.DOWN,
            Button.LEFT,
            Button.RIGHT,
            Button.CENTER
        ]


class Controller:

    def __init__(self):
        self.buttons = ButtonStates()

        self._button_to_pin_map = {
            Button.A: DigitalInOut(board.D5),
            Button.B: DigitalInOut(board.D6),
            Button.UP: DigitalInOut(board.D17),
            Button.LEFT: DigitalInOut(board.D27),
            Button.RIGHT: DigitalInOut(board.D23),
            Button.DOWN: DigitalInOut(board.D22),
            Button.CENTER: DigitalInOut(board.D4)
        }

        for pin in self._button_to_pin_map.values():
            pin.direction = Direction.INPUT
            pin.pull = Pull.UP

    def update_state(self):
        self.buttons.pressed = []
        self.buttons.released = []

        for button, pin in self._button_to_pin_map.items():
            if not pin.value:
                self.buttons.pressed.append(button)

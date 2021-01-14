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


class Controller:

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

        self._buttons = {
            Button.A: DigitalInOut(board.D5),
            Button.B: DigitalInOut(board.D6),
            Button.UP: DigitalInOut(board.D17),
            Button.LEFT: DigitalInOut(board.D27),
            Button.RIGHT: DigitalInOut(board.D23),
            Button.DOWN: DigitalInOut(board.D22),
            Button.CENTER: DigitalInOut(board.D4)
        }

        for button in self._buttons.values():
            button.direction = Direction.INPUT
            button.pull = Pull.UP

    def read_state(self):
        self.pressed = []
        self.released = []

        for key, button in self._buttons.items():
            if not button.value:
                self.pressed.append(key)

import board
import busio

import adafruit_ssd1306

from digitalio import DigitalInOut
from digitalio import Direction
from digitalio import Pull

import enum


class Button(enum.Enum):
    A = 'A'
    B = 'B'
    UP = 'U'
    LEFT = 'L'
    RIGHT = 'R'
    DOWN = 'D'
    CENTER = 'M'


button_A = DigitalInOut(board.D5)
button_A.direction = Direction.INPUT
button_A.pull = Pull.UP

button_B = DigitalInOut(board.D6)
button_B.direction = Direction.INPUT
button_B.pull = Pull.UP

button_U = DigitalInOut(board.D17)
button_U.direction = Direction.INPUT
button_U.pull = Pull.UP

button_L = DigitalInOut(board.D27)
button_L.direction = Direction.INPUT
button_L.pull = Pull.UP

button_R = DigitalInOut(board.D23)
button_R.direction = Direction.INPUT
button_R.pull = Pull.UP

button_D = DigitalInOut(board.D22)
button_D.direction = Direction.INPUT
button_D.pull = Pull.UP

button_C = DigitalInOut(board.D4)
button_C.direction = Direction.INPUT
button_C.pull = Pull.UP


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

    def read_state(self):
        self.pressed = []
        self.released = []

        if not button_A.value:
            self.pressed.append(Button.A)

        if not button_B.value:
            self.pressed.append(Button.B)

        if not button_U.value:
            self.pressed.append(Button.UP)

        if not button_L.value:
            self.pressed.append(Button.LEFT)

        if not button_R.value:
            self.pressed.append(Button.RIGHT)

        if not button_D.value:
            self.pressed.append(Button.DOWN)

        if not button_C.value:
            self.pressed.append(Button.CENTER)

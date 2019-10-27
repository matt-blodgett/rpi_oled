import board

from digitalio import DigitalInOut
from digitalio import Direction
from digitalio import Pull

from .base import Button
from .base import BaseController


class OledController(BaseController):

    def __init__(self):
        super().__init__()

        self._oled_buttons = {
            Button.A: DigitalInOut(board.D5),
            Button.B: DigitalInOut(board.D6),
            Button.UP: DigitalInOut(board.D17),
            Button.LEFT: DigitalInOut(board.D27),
            Button.RIGHT: DigitalInOut(board.D23),
            Button.DOWN: DigitalInOut(board.D22),
            Button.CENTER: DigitalInOut(board.D4)
        }

        for button in self._oled_buttons:
            button.direction = Direction.INPUT
            button.pull = Pull.UP

    def read_state(self):
        self.pressed = []
        self.released = []

        for key, button in self._oled_buttons.items():
            if not button.value:
                self.pressed.append(key)

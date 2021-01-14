import typing
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

    def update(self) -> None:
        for button, pin in self._button_to_pin_map.items():
            if not pin.value:
                self.buttons_pressed.append(button)
            else:
                self.buttons_released.append(button)

    def is_pressed(self, button: Button) -> bool:
        return button in self.buttons_pressed

    def is_released(self, button: Button) -> bool:
        return button in self.buttons_released

    def is_pressed_all(self, buttons: typing.List[Button]) -> bool:
        for button in buttons:
            if button not in self.buttons_pressed:
                return False
        return True

    def is_released_all(self, buttons: typing.List[Button]) -> bool:
        for button in buttons:
            if button not in self.buttons_released:
                return False
        return True

    def is_pressed_any(self, buttons: typing.List[Button]) -> bool:
        for button in buttons:
            if button in self.buttons_pressed:
                return True
        return False

    def is_released_any(self, buttons: typing.List[Button]) -> bool:
        for button in buttons:
            if button in self.buttons_released:
                return True
        return False

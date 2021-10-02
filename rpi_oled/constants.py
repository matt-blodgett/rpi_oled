import enum


class Button(enum.Enum):
    A = 'A'
    B = 'B'
    UP = 'U'
    LEFT = 'L'
    RIGHT = 'R'
    DOWN = 'D'
    CENTER = 'M'
    NULL = 'NULL'


DISPLAY_WIDTH = 128
DISPLAY_HEIGHT = 64


PATH_SETTINGS_FILE = './settings.json'

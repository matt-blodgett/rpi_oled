import os
import json
import time
import threading

from PIL import Image
from PIL import ImageDraw
from PIL import ImageOps

from .constants import Button
from .constants import PATH_SETTINGS_FILE

from .components import Menu
from .components import Page
from .components import PageSettings


class PageLoading(Page):

    def __init__(self, id, parent):
        super().__init__(id, parent)

        self._loading = True

    def _animate(self, index, total, step, delay):
        if index == total:
            self._loading = False
            image = self.render()
            self.emit_event('image', image)
        else:
            index += step

            if index > total:
                index = total

            image = self.get_empty_image()
            draw = ImageDraw.Draw(image)

            draw.rectangle(((1, 1), (self.width - 2, self.height - 2)), fill=None, width=1, outline='#000000')
            draw.text((20, 20), f'Loading - {index}%', font=self.font, fill='#FFFFFF')

            self.emit_event('image', image)

            time.sleep(delay / 1000)
            self._animate(index, total, step, delay)

    def mounted(self):
        self._loading = True
        thread = threading.Thread(target=self._animate, args=(0, 100, 2, 10), daemon=True)
        thread.start()

    def unmounted(self):
        self._loading = False

    def render(self):
        image = self.get_empty_image()
        draw = ImageDraw.Draw(image)

        draw.text((20, 20), 'Welcome Screen', font=self.font, fill='#FFFFFF')

        return image

    def update(self, button):
        if self._loading:
            return

        if button is Button.A:
            self.emit_event('component', 'menu-0')
            return

        elif button is Button.B:
            return

        elif button is Button.UP:
            return

        elif button is Button.LEFT:
            return

        elif button is Button.RIGHT:
            return

        elif button is Button.DOWN:
            return

        elif button is Button.CENTER:
            return

        elif button is Button.NULL:
            return

        image = self.render()
        self.emit_event('image', image)


class PageAnimation(Page):

    def __init__(self, id, parent):
        super().__init__(id, parent)

        self._cancel = True

    def _animate(self, count, delay, index=0):
        if not self._cancel:
            index += 1
            if index <= count:
                image = self.get_empty_image()

                draw = ImageDraw.Draw(image)
                draw.text((1, 1), f'{index} of {count}', font=self.font, fill='#FFFFFF')

                self.emit_event('image', image)

                time.sleep(delay / 1000)
                self._animate(count, delay, index=index)
        else:
            image = self.render()
            self.emit_event('image', image)

    def mounted(self):
        self._cancel = False
        super().mounted()

    def unmounted(self):
        self._cancel = True

    def render(self):
        image = self.get_empty_image()
        draw = ImageDraw.Draw(image)

        draw.text((20, 20), 'Animation Page', font=self.font, fill='#FFFFFF')

        return image

    def update(self, button):
        if button is Button.A:
            return

        elif button is Button.B:
            self._cancel = True
            self.emit_event('back')
            return

        elif button is Button.UP:
            self._cancel = False
            thread = threading.Thread(target=self._animate, args=(10, 500), daemon=True)
            thread.start()
            return

        elif button is Button.LEFT:
            return

        elif button is Button.RIGHT:
            return

        elif button is Button.DOWN:
            self._cancel = True
            return

        elif button is Button.CENTER:
            return

        elif button is Button.NULL:
            return

        image = self.render()
        self.emit_event('image', image)


class PageHome(Page):

    def __init__(self, id, parent):
        super().__init__(id, parent)

        self._selected_tile = [0, 0]

        dir_base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        dir_icons = f'{dir_base}/icons'

        self.icon_bluetooth = Image.open(f'{dir_icons}/baseline_bluetooth_white_18dp.png')
        self.icon_folder = Image.open(f'{dir_icons}/baseline_folder_white_18dp.png')
        self.icon_power = Image.open(f'{dir_icons}/baseline_power_settings_new_white_18dp.png')
        self.icon_settings = Image.open(f'{dir_icons}/baseline_settings_white_18dp.png')
        self.icon_sync = Image.open(f'{dir_icons}/baseline_sync_white_18dp.png')
        self.icon_wifi = Image.open(f'{dir_icons}/baseline_wifi_white_18dp.png')

    def mounted(self):
        super().mounted()

    def unmounted(self):
        pass

    def render(self):
        image = self.get_empty_image()
        draw = ImageDraw.Draw(image)
        # font = self.font

        x_units = self.width / 3
        y_units = self.height / 2
        coords_vertical_1 = ((x_units * 1, 0), (x_units * 1, self.height))
        coords_vertical_2 = ((x_units * 2, 0), (x_units * 2, self.height))
        coords_horizontal_1 = ((0, y_units * 1), (self.width, y_units * 1))

        draw.line(coords_vertical_1, fill='#FFFFFF', width=1)
        draw.line(coords_vertical_2, fill='#FFFFFF', width=1)
        draw.line(coords_horizontal_1, fill='#FFFFFF', width=1)
        draw.rectangle(((0, 0), (self.width - 1, self.height - 1)), fill=None, width=1, outline='#FFFFFF')

        x_offset, y_offset = self._selected_tile
        draw.rectangle(((x_units * x_offset, y_units * y_offset), (x_units * (x_offset + 1), y_units * (y_offset + 1))), fill='#FFFFFF', width=1)

        icons = [
            [self.icon_bluetooth, self.icon_folder, self.icon_power],
            [self.icon_settings, self.icon_sync, self.icon_wifi]
        ]

        icon = icons[y_offset][x_offset]
        icon = icon.convert('L')
        icon_inverted = ImageOps.invert(icon)
        icons[y_offset][x_offset] = icon_inverted

        image.paste(icons[0][0], (10, 10))
        image.paste(icons[0][1], (55, 10))
        image.paste(icons[0][2], (100, 10))
        image.paste(icons[1][0], (10, 40))
        image.paste(icons[1][1], (55, 40))
        image.paste(icons[1][2], (100, 40))

        return image

    def update(self, button):
        if button is Button.A:
            x, y = self._selected_tile
            if x == 0 and y == 0:
                print('bluetooth')
            elif x == 1 and y == 0:
                print('folder')
            elif x == 2 and y == 0:
                print('power')
            elif x == 0 and y == 1:
                print('settings')
            elif x == 1 and y == 1:
                print('sync')
            elif x == 2 and y == 1:
                print('wifi')
            return

        elif button is Button.B:
            self.emit_event('back')
            return

        elif button is Button.UP:
            if self._selected_tile[1] > 0:
                self._selected_tile[1] -= 1
            else:
                return

        elif button is Button.LEFT:
            if self._selected_tile[0] > 0:
                self._selected_tile[0] -= 1
            else:
                return

        elif button is Button.RIGHT:
            if self._selected_tile[0] < 2:
                self._selected_tile[0] += 1
            else:
                return

        elif button is Button.DOWN:
            if self._selected_tile[1] < 1:
                self._selected_tile[1] += 1
            else:
                return

        elif button is Button.CENTER:
            return

        elif button is Button.NULL:
            return

        image = self.render()
        self.emit_event('image', image)


class ApplicationConfig:

    def __init__(self):
        self.settings = {}
        self.components = {}
        self.initial_component = None

    def _load_settings(self, setting_items):
        if os.path.exists(PATH_SETTINGS_FILE):
            with open(PATH_SETTINGS_FILE, 'r') as i_file:
                file_settings = json.loads(i_file.read())
                for settings in setting_items:
                    for setting in settings:
                        if setting['key'] is not None:
                            setting['value'] = file_settings.get(setting['key'], setting['value'])

    def initialize(self):
        menu_items = [
            [
                {'label': 'MAIN MENU', 'child': 'page-5'},
                {'label': 'settings 1', 'child': 'page-3'},
                {'label': 'settings 2', 'child': 'page-4'},
                {'label': 'animation page', 'child': 'page-2'},
                {'label': 'menu 1', 'child': 'menu-1'},
                {'label': 'page 1', 'child': 'page-0'},
                {'label': 'page 2', 'child': 'page-1'},
                {'label': 'action 1', 'child': None}
            ],
            [
                {'label': 'MENU #2', 'child': None},
                {'label': 'menu 3', 'child': 'menu-2'},
                {'label': 'page 1', 'child': 'page-0'},
                {'label': 'none', 'child': None},
                {'label': 'none', 'child': None},
                {'label': 'menu 4', 'child': 'menu-3'}
            ],
            [
                {'label': 'Menu #3', 'child': None},
                {'label': 'page 1', 'child': 'page-0'},
                {'label': 'none', 'child': None}
            ],
            [
                {'label': 'Menu #4', 'child': None},
                {'label': 'page 1', 'child': 'page-0'},
                {'label': 'none', 'child': None}
            ]
        ]

        setting_items = [
            [
                {'label': 'Integer #1', 'type': 'integer', 'key': 'key-0-0', 'value': 0, 'options': {'min_value': 0, 'max_value': 100}},
                {'label': 'Select #1', 'type': 'select', 'key': 'key-0-1', 'value': '', 'options': {'choices': ['', 'A', 'B', 'C']}},
                {'label': 'Toggle #1', 'type': 'toggle', 'key': 'key-0-2', 'value': False},
                {'label': 'Toggle #2', 'type': 'toggle', 'key': 'key-0-3', 'value': False},
                {'label': 'Toggle #3', 'type': 'toggle', 'key': 'key-0-4', 'value': False},
                {'label': 'Toggle #4', 'type': 'toggle', 'key': 'key-0-5', 'value': False},
                {'label': 'Toggle #5', 'type': 'toggle', 'key': 'key-0-6', 'value': False},
                {'label': 'Save', 'type': 'save', 'key': None, 'value': None},
                {'label': 'Cancel', 'type': 'cancel', 'key': None, 'value': None}
            ],
            [
                {'label': 'Setting #1', 'type': 'toggle', 'key': 'key-1-0', 'value': False},
                {'label': 'Setting #2', 'type': 'toggle', 'key': 'key-1-1', 'value': False},
                {'label': 'Setting #3', 'type': 'toggle', 'key': 'key-1-2', 'value': False},
                {'label': 'Setting #4', 'type': 'toggle', 'key': 'key-1-3', 'value': False},
                {'label': 'Setting #5', 'type': 'toggle', 'key': 'key-1-4', 'value': False},
                {'label': 'Save', 'type': 'save', 'key': None, 'value': None},
                {'label': 'Cancel', 'type': 'cancel', 'key': None, 'value': None}
            ]
        ]

        self._load_settings(setting_items)

        components = [
            Menu('menu-0', None, menu_items[0]),
            Menu('menu-1', 'menu-0', menu_items[1]),
            Menu('menu-2', 'menu-1', menu_items[2]),
            Menu('menu-3', 'menu-1', menu_items[3]),
            Page('page-0', None),
            Page('page-1', None),
            PageAnimation('page-2', None),
            PageSettings('page-3', None, setting_items[0], title='Connection Settings'),
            PageSettings('page-4', None, setting_items[1], title='Preference Settings'),
            PageHome('page-5', None)
        ]

        self.settings = {}
        for settings in setting_items:
            for setting in settings:
                if setting['key'] is not None:
                    self.settings[setting['key']] = setting['value']

        self.components = {component.id: component for component in components}
        self.initial_component = PageLoading(None, None)

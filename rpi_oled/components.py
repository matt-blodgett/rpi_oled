from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

from .constants import Button
from .constants import DISPLAY_WIDTH
from .constants import DISPLAY_HEIGHT


# DISPLAY_FONT = ImageFont.truetype('arial.ttf', 9)
DISPLAY_FONT = ImageFont.load_default()


# draw.text((4, 4), 'Menu Item Number 1', font=self.font, fill='#FFFFFF')
# draw.rectangle((1, 10, 20, 30), fill=None, outline='#FFFFFF', width=1)
# draw.line(((1, 1), (DISPLAY_WIDTH, 1)), width=1, fill='#FFFFFF')
# draw.ellipse(((0, 0), (6, 6)), width=1, fill='#FFFFFF')

# self.font_bold = ImageFont.truetype('arialbd.ttf', 10)
# self.font = ImageFont.truetype('consola.ttf', 10)
# self.font_bold = ImageFont.truetype('consolab.ttf', 10)


class Component:

    def __init__(self, id, parent):
        self.id = id
        self.parent = parent

        self.image = None

        self.emit_event = lambda event, *args: None

    @property
    def width(self):
        return DISPLAY_WIDTH

    @property
    def height(self):
        return DISPLAY_HEIGHT

    @property
    def font(self):
        return DISPLAY_FONT

    @staticmethod
    def get_empty_image():
        return Image.new('1', (DISPLAY_WIDTH, DISPLAY_HEIGHT), color=0)

    def mounted(self):
        image = self.render()
        self.emit_event('image', image)

    def unmounted(self):
        pass

    def render(self):
        raise NotImplementedError

    def update(self, button):
        raise NotImplementedError


class Page(Component):

    def __init__(self, id, parent):
        super().__init__(id, parent)

    def mounted(self):
        super().mounted()

    def unmounted(self):
        pass

    def render(self):
        image = self.get_empty_image()
        draw = ImageDraw.Draw(image)
        font = self.font

        draw.text((20, 20), 'Page Mode', font=font, fill='#FFFFFF')
        draw.text((20, 40), f'Page ID: {self.id}', font=font, fill='#FFFFFF')

        return image

    def update(self, button):
        if button is Button.A:
            print('A')

        elif button is Button.B:
            print('B')
            self.emit_event('back')
            return

        elif button is Button.UP:
            print('UP')

        elif button is Button.LEFT:
            print('LEFT')

        elif button is Button.RIGHT:
            print('RIGHT')

        elif button is Button.DOWN:
            print('DOWN')

        elif button is Button.CENTER:
            print('CENTER')

        elif button is Button.NULL:
            print('NULL')

        image = self.render()
        self.emit_event('image', image)


class PageSettings(Page):

    def __init__(self, id, parent, items, title=None):
        super().__init__(id, parent)

        for idx, setting in enumerate(items):
            setting['id'] = idx

        self._settings = items
        self._settings_pre_save = []
        for setting in self._settings:
            if setting['key'] is not None:
                self._settings_pre_save.append({'id': setting['id'], 'value': setting['value']})

        self._items = self._settings
        self._items_display = self._items[:3]
        self._item_index = 0
        self._cursor_index = 0

        self._selected_setting = None

        self.title = title or 'Settings Page'

    def _scroll(self, direction):
        item_count = len(self._items)

        self._item_index += direction
        self._cursor_index += direction

        if self._item_index < 0:
            self._item_index = 0
        elif self._item_index == item_count:
            self._item_index = item_count - 1

        if self._cursor_index < 0:
            self._cursor_index = 0
        elif self._cursor_index == 3:
            self._cursor_index = 2

        if item_count < 3:
            self._cursor_index = self._item_index

        if self._item_index == 0:
            self._items_display = self._items[:3]
        elif self._item_index == item_count - 1:
            self._items_display = self._items[-3:]
        else:
            self._items_display = [self._items[self._item_index]]
            if self._cursor_index == 0:
                self._items_display.append(self._items[self._item_index + 1])
                self._items_display.append(self._items[self._item_index + 2])
            elif self._cursor_index == 1:
                self._items_display.insert(0, self._items[self._item_index - 1])
                self._items_display.append(self._items[self._item_index + 1])
            elif self._cursor_index == 2:
                self._items_display.insert(0, self._items[self._item_index - 1])
                self._items_display.insert(0, self._items[self._item_index - 2])

    def _settings_save(self):
        for setting in self._settings:
            if setting['key'] is not None:
                self.emit_event('setting', setting['key'], setting['value'])
            for setting_pre_save in self._settings_pre_save:
                if setting['id'] == setting_pre_save['id']:
                    setting_pre_save['value'] = setting['value']
                    break

    def _settings_reset(self):
        for setting in self._settings:
            for setting_pre_save in self._settings_pre_save:
                if setting['id'] == setting_pre_save['id']:
                    setting['value'] = setting_pre_save['value']
                    break

    def mounted(self):
        super().mounted()

    def unmounted(self):
        self._items = self._settings
        self._items_display = self._items[:3]
        self._item_index = 0
        self._cursor_index = 0

    def render(self):
        image = self.get_empty_image()
        draw = ImageDraw.Draw(image)
        font = self.font

        draw.text((1, 1), self.title, font=self.font, fill='#FFFFFF')
        draw.line(((1, 14), (self.width, 14)), fill='#FFFFFF', width=1)

        x = 7
        y = 18
        y_padding = 15

        for setting in self._items_display:
            y_cursor = y

            width = 1
            if self._selected_setting == self._item_index:
                if self._items[self._item_index]['id'] == setting['id']:
                    width = 2

            if setting['type'] == 'toggle':
                draw.text((x, y), setting['label'], font=font, fill='#FFFFFF')
                draw.rectangle(((self.width - 40, y), (self.width - 6, y + y_padding - 4)), fill=None, width=width, outline='#FFFFFF')
                text = 'Y' if setting['value'] else 'N'
                draw.text((self.width - 18, y), text, font=font, fill='#FFFFFF')

            elif setting['type'] == 'integer':
                draw.text((x, y), setting['label'], font=font, fill='#FFFFFF')
                draw.rectangle(((self.width - 40, y), (self.width - 6, y + y_padding - 4)), fill=None, width=width, outline='#FFFFFF')
                x_offset = len(str(setting['value'])) + (1 * len(str(setting['value'])))
                draw.text((self.width - 17 - x_offset, y), str(setting['value']), font=font, fill='#FFFFFF')

            elif setting['type'] == 'select':
                draw.text((x, y), setting['label'], font=font, fill='#FFFFFF')
                draw.rectangle(((self.width - 40, y), (self.width - 6, y + y_padding - 4)), fill=None, width=width, outline='#FFFFFF')
                x_offset = len(str(setting['value'])) + (1 * len(str(setting['value'])))
                draw.text((self.width - 17 - x_offset, y), str(setting['value']), font=font, fill='#FFFFFF')

            elif setting['type'] == 'save':
                draw.line(((0, y + 2), (self.width, y + 2)), fill='#FFFFFF', width=1)
                draw.text((x, y + 3), setting['label'], font=font, fill='#FFFFFF')
                y_cursor += 3

            elif setting['type'] == 'cancel':
                draw.text((x, y + 2), setting['label'], font=font, fill='#FFFFFF')
                y_cursor += 2

            else:
                draw.text((x, y), setting['label'], font=font, fill='#FFFFFF')

            if self._items[self._item_index]['id'] == setting['id']:
                draw.text((1, y_cursor), '>', font=font, fill='#FFFFFF')

            y += y_padding

        return image

    def update(self, button):
        if button is Button.A:
            item = self._items[self._item_index]

            if item['type'] == 'save':
                self._settings_save()
                self.emit_event('back')
                return

            elif item['type'] == 'cancel':
                self._settings_reset()
                self.emit_event('back')
                return

            if self._selected_setting is None:
                self._selected_setting = self._item_index
            else:
                if item['type'] == 'toggle':
                    item['value'] = not item['value']

        elif button is Button.B:
            if self._selected_setting is not None:
                self._selected_setting = None
            else:
                self._settings_reset()
                self.emit_event('back')
                return

        elif button is Button.UP:
            if self._selected_setting is None:
                self._scroll(-1)
            else:
                item = self._items[self._item_index]
                if item['type'] == 'toggle':
                    item['value'] = True
                elif item['type'] == 'integer':
                    item['value'] += 1
                elif item['type'] == 'select':
                    idx = item['options']['choices'].index(item['value'])
                    idx -= 1
                    if idx < 0:
                        idx = 0
                    item['value'] = item['options']['choices'][idx]

        elif button is Button.LEFT:
            self._selected_setting = None

        elif button is Button.RIGHT:
            self._selected_setting = self._item_index

        elif button is Button.DOWN:
            if self._selected_setting is None:
                self._scroll(1)
            else:
                item = self._items[self._item_index]
                if item['type'] == 'toggle':
                    item['value'] = False
                elif item['type'] == 'integer':
                    item['value'] -= 1
                elif item['type'] == 'select':
                    idx = item['options']['choices'].index(item['value'])
                    idx += 1
                    if idx >= len(item['options']['choices']):
                        idx = len(item['options']['choices']) - 1
                    item['value'] = item['options']['choices'][idx]

        elif button is Button.CENTER:
            return

        elif button is Button.NULL:
            return

        image = self.render()
        self.emit_event('image', image)


class Menu(Component):

    def __init__(self, id, parent, items):
        super().__init__(id, parent)

        for idx, item in enumerate(items):
            item['id'] = idx

        self._items = items
        self._items_display = items[:3]
        self._item_index = 0
        self._cursor_index = 0

    def _scroll(self, direction):
        item_count = len(self._items)

        self._item_index += direction
        self._cursor_index += direction

        if self._item_index < 0:
            self._item_index = 0
        elif self._item_index == item_count:
            self._item_index = item_count - 1

        if self._cursor_index < 0:
            self._cursor_index = 0
        elif self._cursor_index == 3:
            self._cursor_index = 2

        if item_count < 3:
            self._cursor_index = self._item_index

        if self._item_index == 0:
            self._items_display = self._items[:3]
        elif self._item_index == item_count - 1:
            self._items_display = self._items[-3:]
        else:
            self._items_display = [self._items[self._item_index]]
            if self._cursor_index == 0:
                self._items_display.append(self._items[self._item_index + 1])
                self._items_display.append(self._items[self._item_index + 2])
            elif self._cursor_index == 1:
                self._items_display.insert(0, self._items[self._item_index - 1])
                self._items_display.append(self._items[self._item_index + 1])
            elif self._cursor_index == 2:
                self._items_display.insert(0, self._items[self._item_index - 1])
                self._items_display.insert(0, self._items[self._item_index - 2])

    def mounted(self):
        super().mounted()

    def unmounted(self):
        pass

    def render(self):
        image = self.get_empty_image()
        draw = ImageDraw.Draw(image)
        font = self.font

        item_count = len(self._items)

        draw.rectangle(((1, 1), (self.width - 2, self.height - 2)), fill=None, width=1, outline='#FFFFFF')

        x = 16
        start = 7
        spacing = 18
        y0 = start
        y1 = start + spacing
        y2 = start + spacing + spacing + 2

        if self._items_display[0]['id'] == self._items[0]['id']:
            draw.rectangle(((1, 1), (self.width - 2, y1 - 6)), fill='#FFFFFF', width=1, outline=None)
            draw.text((x, y0), self._items_display[0]['label'], font=font, fill='#000000')
        else:
            draw.text((x, y0), self._items_display[0]['label'], font=font, fill='#FFFFFF')

        if item_count > 1:
            draw.text((x, y1), self._items_display[1]['label'], font=font, fill='#FFFFFF')
        if item_count > 2:
            draw.text((x, y2), self._items_display[2]['label'], font=font, fill='#FFFFFF')

        x = 6
        y = [y0, y1, y2][self._cursor_index]
        cursor_fill = '#FFFFFF'
        if self._items_display[0]['id'] == self._items[0]['id'] and self._cursor_index == 0:
            cursor_fill = '#000000'
        draw.text((x, y), '>', font=font, fill=cursor_fill)

        y0 += 14
        y1 += 16
        draw.line(((1, y0), (self.width, y0)), fill='#FFFFFF', width=1)
        draw.line(((1, y1), (self.width, y1)), fill='#FFFFFF', width=1)

        return image

    def update(self, button):
        if button is Button.A:
            child = self._items[self._item_index]['child']
            if child is not None:
                self.emit_event('component', child)
                return

        elif button is Button.B:
            self.emit_event('back')
            return

        elif button is Button.UP:
            self._scroll(-1)

        elif button is Button.LEFT:
            return

        elif button is Button.RIGHT:
            return

        elif button is Button.DOWN:
            self._scroll(1)

        elif button is Button.CENTER:
            return

        elif button is Button.NULL:
            pass

        image = self.render()
        self.emit_event('image', image)

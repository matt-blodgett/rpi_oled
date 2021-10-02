import os
import json

import tkinter as tk

from PIL import ImageTk

from .constants import Button
from .constants import DISPLAY_WIDTH
from .constants import DISPLAY_HEIGHT
from .constants import PATH_SETTINGS_FILE


class FrameDisplay(tk.Frame):

    def __init__(self, master):
        super().__init__(master)

        config = {
            'width': DISPLAY_WIDTH,
            'height': DISPLAY_HEIGHT,
            'border': 0,
            'borderwidth': 0,
            'highlightthickness': 0,
            'highlightbackground': '#FFFFFF',
            'background': '#777777'
        }
        self.configure(**config)

        self.grid_propagate(False)

        self.lbl_display = tk.Label(self)
        self.lbl_display.grid(row=0, column=0, sticky=tk.NSEW)
        self.lbl_display.configure(**config)


class FrameButtons(tk.Frame):

    def __init__(self, master):
        super().__init__(master)

        config = {
            'border': 10,
            'highlightthickness': 1,
            'highlightbackground': '#888888',
            'background': '#DDDDDD'
        }
        self.configure(**config)

        self.btn_a = tk.Button(self)
        self.btn_b = tk.Button(self)
        self.btn_up = tk.Button(self)
        self.btn_left = tk.Button(self)
        self.btn_right = tk.Button(self)
        self.btn_down = tk.Button(self)
        self.btn_center = tk.Button(self)

        self.grid_rowconfigure(0, minsize=20, weight=1)
        self.grid_rowconfigure(1, minsize=20, weight=1)
        self.grid_rowconfigure(2, minsize=20, weight=1)

        self.grid_columnconfigure(0, minsize=20, weight=1)
        self.grid_columnconfigure(1, minsize=20, weight=1)
        self.grid_columnconfigure(2, minsize=20, weight=1)
        self.grid_columnconfigure(3, minsize=20, weight=1)
        self.grid_columnconfigure(4, minsize=20, weight=1)
        self.grid_columnconfigure(5, minsize=20, weight=1)
        self.grid_columnconfigure(6, minsize=20, weight=1)

        self.btn_a.grid(row=0, column=6, sticky=tk.NSEW)
        self.btn_b.grid(row=1, column=5, sticky=tk.NSEW)
        self.btn_up.grid(row=0, column=1, sticky=tk.NSEW)
        self.btn_left.grid(row=1, column=0, sticky=tk.NSEW)
        self.btn_right.grid(row=1, column=2, sticky=tk.NSEW)
        self.btn_down.grid(row=2, column=1, sticky=tk.NSEW)
        self.btn_center.grid(row=1, column=1, sticky=tk.NSEW)

        config = {
            'width': 4,
            'height': 2,
            'background': '#BFBFBF',
            'font': ('Helvetica', 10)
        }
        self.btn_a.configure(text='A', **config)
        self.btn_b.configure(text='B', **config)
        self.btn_up.configure(text='↑', **config)
        self.btn_left.configure(text='←', **config)
        self.btn_right.configure(text='→', **config)
        self.btn_down.configure(text='↓', **config)
        self.btn_center.configure(text='O', **config)


class RootWindow(tk.Tk):

    def __init__(self, state):
        super().__init__()

        self._state = state

        self.frm_main = tk.Frame(self)
        self.frm_display = FrameDisplay(self.frm_main)
        self.frm_buttons = FrameButtons(self.frm_main)
        self.canvas = self.frm_display.lbl_display

        self._initialize()
        self._initialize_menu_bar()

        self._state.initialize(self._update_display)

    def _initialize(self):
        self.title('rpi oled')
        self.minsize(300, 300)
        self.maxsize(600, 600)
        self.geometry('+800+100')

        self.grid_rowconfigure(0, minsize=0, weight=1)
        self.grid_columnconfigure(0, minsize=0, weight=1)

        self.frm_main.grid(row=0, column=0, sticky=tk.NSEW)

        self.frm_main.grid_rowconfigure(0, minsize=20, weight=1)
        self.frm_main.grid_rowconfigure(1, minsize=0, weight=0)
        self.frm_main.grid_rowconfigure(2, minsize=30, weight=0)
        self.frm_main.grid_rowconfigure(3, minsize=0, weight=0)
        self.frm_main.grid_rowconfigure(4, minsize=20, weight=1)

        self.frm_main.grid_columnconfigure(0, minsize=20, weight=1)
        self.frm_main.grid_columnconfigure(1, minsize=0, weight=0)
        self.frm_main.grid_columnconfigure(2, minsize=20, weight=1)

        self.frm_display.grid(row=1, column=1, sticky=tk.NS)
        self.frm_buttons.grid(row=3, column=1, sticky=tk.NSEW)

        self.frm_main.configure(background='#CFCFCF')

        self.frm_buttons.btn_a.bind('<ButtonRelease-1>', lambda e: self._on_button_released(Button.A))
        self.frm_buttons.btn_b.bind('<ButtonRelease-1>', lambda e: self._on_button_released(Button.B))
        self.frm_buttons.btn_up.bind('<ButtonRelease-1>', lambda e: self._on_button_released(Button.UP))
        self.frm_buttons.btn_left.bind('<ButtonRelease-1>', lambda e: self._on_button_released(Button.LEFT))
        self.frm_buttons.btn_right.bind('<ButtonRelease-1>', lambda e: self._on_button_released(Button.RIGHT))
        self.frm_buttons.btn_down.bind('<ButtonRelease-1>', lambda e: self._on_button_released(Button.DOWN))
        self.frm_buttons.btn_center.bind('<ButtonRelease-1>', lambda e: self._on_button_released(Button.CENTER))
        self.bind('<KeyRelease>', self._on_key_released)

    def _initialize_menu_bar(self):
        def _cmd_file_reset():
            self._state.reset()

        def _cmd_file_exit():
            self.quit()

        def _cmd_settings_write():
            with open(PATH_SETTINGS_FILE, 'w') as o_file:
                o_file.write(json.dumps(self._state.settings, indent=2))

        def _cmd_settings_open():
            if os.path.exists(PATH_SETTINGS_FILE):
                os.system(f'start notepad++ {PATH_SETTINGS_FILE}')

        def _cmd_settings_print():
            print(self._state.settings)

        def _cmd_help_about():
            print('help - about')

        menu_bar = tk.Menu(self)

        menu_file = tk.Menu(menu_bar, tearoff=False)
        menu_file.add_command(label='Reset', command=_cmd_file_reset)
        menu_file.add_separator()
        menu_file.add_command(label='Exit', command=_cmd_file_exit)
        menu_bar.add_cascade(label='File', menu=menu_file)

        menu_settings = tk.Menu(menu_bar, tearoff=False)
        menu_settings.add_command(label='Write', command=_cmd_settings_write)
        menu_settings.add_command(label='Open', command=_cmd_settings_open)
        menu_settings.add_command(label='Print', command=_cmd_settings_print)
        menu_bar.add_cascade(label='Settings', menu=menu_settings)

        menu_help = tk.Menu(menu_bar, tearoff=False)
        menu_help.add_command(label='About', command=_cmd_help_about)
        menu_bar.add_cascade(label='Help', menu=menu_help)

        self.config(menu=menu_bar)

    def _update_display(self, image):
        image_tk = ImageTk.PhotoImage(image)
        self.canvas.configure(image=image_tk)
        self.canvas.image = image_tk
        self.update_idletasks()

    def _on_button_released(self, button):
        self._state.update(button)

    def _on_key_released(self, event):
        keycode_map = {
            37: Button.LEFT,
            38: Button.UP,
            39: Button.RIGHT,
            40: Button.DOWN,
            97: Button.B,
            101: Button.A,
            13: Button.A
        }
        button = keycode_map.get(event.keycode, None)
        if button:
            self._on_button_released(button)

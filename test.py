import tkinter as tk

from PIL import Image
from PIL import ImageTk
from PIL import ImageDraw


class RootWindow(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)

        self.display = tk.Label(self)
        self.display.grid(row=0, column=0, sticky=tk.NSEW)

    def set_display(self, image):
        self.display_image = ImageTk.PhotoImage(image=image)
        self.display.config(image=self.display_image)


def main():
    root = RootWindow()

    width = 128
    height = 64

    image = Image.new('1', (width, height))
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    root.set_display(image)
    root.mainloop()


if __name__ == '__main__':
    main()

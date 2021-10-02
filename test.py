from rpi_oled.config import ApplicationConfig
from rpi_oled.state import ApplicationState
from rpi_oled.tkui import RootWindow


def main():
    config = ApplicationConfig()
    state = ApplicationState(config)
    root = RootWindow(state)
    root.mainloop()


if __name__ == '__main__':
    main()

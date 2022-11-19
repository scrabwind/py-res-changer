import pystray
import pywintypes
import win32api
import win32con
from PIL import Image
from pystray import MenuItem

from src.dpi_change import set_dpi
from src.toggle_listen import on_listen_start, on_listen_stop

state = False


def on_set_resolution(width: int, height: int, dpi: int):
    set_dpi(dpi)
    devmode = pywintypes.DEVMODEType()
    devmode.PelsWidth = width
    devmode.PelsHeight = height

    devmode.Fields = win32con.DM_PELSWIDTH | win32con.DM_PELSHEIGHT

    win32api.ChangeDisplaySettings(devmode, 0)


def on_clicked(icon, item):
    global state
    state = not item.checked
    if state:
        on_listen_start()
    else:
        on_listen_stop()


def on_quit():
    icon.visible = False
    icon.stop()


if __name__ == "__main__":
    image = Image.open("../assets/peepo.png")

    menu = (
        MenuItem('1440p', lambda: on_set_resolution(2560, 1440, 125)),
        MenuItem('1080p', lambda: on_set_resolution(1920, 1080, 100)),
        MenuItem("PS5 Sound", on_clicked, lambda item: state),
        MenuItem('Quit', on_quit)
    )

    icon = pystray.Icon("Resolution Switcher", image, "Resolution Switcher", menu)
    icon.run()

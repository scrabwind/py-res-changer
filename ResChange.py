import pystray
import pywintypes
import win32api
import win32con
from PIL import Image
from pystray import MenuItem as item
from DpiChange import set_dpi


def on_set_resolution(width: int, height: int, dpi: int):
    set_dpi(dpi)
    devmode = pywintypes.DEVMODEType()
    devmode.PelsWidth = width
    devmode.PelsHeight = height

    devmode.Fields = win32con.DM_PELSWIDTH | win32con.DM_PELSHEIGHT

    win32api.ChangeDisplaySettings(devmode, 0)


def on_quit():
    icon.visible = False
    icon.stop()


if __name__ == "__main__":
    image = Image.open("peepo.png")

    menu = (
        item('1440p', lambda: on_set_resolution(2560, 1440, 125)),
        item('1080p', lambda: on_set_resolution(1920, 1080, 100)),
        item('Quit', on_quit)
    )

    icon = pystray.Icon("Resolution Switcher", image, "Resolution Switcher", menu)
    icon.run()

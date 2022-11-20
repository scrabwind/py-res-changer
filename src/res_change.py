import os
import sys

import pystray
import pywintypes
import win32api
import win32con
from PIL import Image
from pystray import MenuItem

from clone_extend_monitors import clone_monitors, extend_monitors
from dpi_change import set_dpi
from toggle_listen import on_listen_start, on_listen_stop

is_listening = False
is_monitor_cloned = False


def on_set_resolution(width: int, height: int, dpi: int):
    set_dpi(dpi)
    devmode = pywintypes.DEVMODEType()
    devmode.PelsWidth = width
    devmode.PelsHeight = height

    devmode.Fields = win32con.DM_PELSWIDTH | win32con.DM_PELSHEIGHT

    win32api.ChangeDisplaySettings(devmode, 0)


def on_listen(icon, item):
    global is_listening
    is_listening = not item.checked
    if is_listening:
        on_listen_start()
    else:
        on_listen_stop()


def on_monitor_change(icon, item):
    global is_monitor_cloned
    is_monitor_cloned = not item.checked
    if is_monitor_cloned:
        clone_monitors()
    else:
        extend_monitors()


def main():
    def on_quit(item):
        on_listen_stop()
        item.visible = False
        item.stop()

    try:
        icon_folder = os.path.join(sys._MEIPASS, 'assets')
        image = Image.open(icon_folder + "/peepo.png")

        icon = pystray.Icon("Resolution Switcher")

        menu = (
            MenuItem('1440p', lambda: on_set_resolution(2560, 1440, 125)),
            MenuItem('1080p', lambda: on_set_resolution(1920, 1080, 100)),
            MenuItem("PS5 Sound", on_listen, lambda item: is_listening),
            MenuItem("Clone/Extend Monitors", on_monitor_change, lambda item: is_monitor_cloned),
            MenuItem('Quit', lambda: on_quit(icon))
        )

        icon.icon = image
        icon.menu = menu
        icon.title = "Resolution Switcher"

        icon.run()
    except Exception as e:
        raise e

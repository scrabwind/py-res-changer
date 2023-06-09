import os
import subprocess
import sys
from pathlib import Path

import pystray
import pywintypes
import win32api
import win32con
from PIL import Image
from pystray import MenuItem

from dpi_change import set_dpi
from toggle_listen import on_listen_start, on_listen_stop

is_listening = False

bundle_dir = Path.cwd()

if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    bundle_dir = Path(sys._MEIPASS)
else:
    bundle_dir = Path(__file__).parent


def on_clone_extend_monitor():
    exe_folder = os.path.join(bundle_dir, 'external')
    subprocess.run([exe_folder + "/CloneMonitors.exe"], creationflags=0x08000000)


def on_set_resolution(width: int, height: int, dpi: int):
    set_dpi(dpi)
    devmode = pywintypes.DEVMODEType()
    devmode.PelsWidth = width
    devmode.PelsHeight = height

    devmode.Fields = win32con.DM_PELSWIDTH | win32con.DM_PELSHEIGHT

    win32api.ChangeDisplaySettings(devmode, 0)


def on_listen(_icon, item):
    global is_listening
    is_listening = not item.checked
    if is_listening:
        on_listen_start()
    else:
        on_listen_stop()


def on_monitor_change():
    on_clone_extend_monitor()


def main():
    def on_quit(item):
        try:
            on_listen_stop()
            item.visible = False
            item.stop()
        except Exception() as e:
            print(e)
        finally:
            sys.exit(0)

    try:
        icon_folder = os.path.join(bundle_dir, 'assets')
        image = Image.open(icon_folder + "/peepo.png")

        icon = pystray.Icon("Resolution Switcher")

        menu = (
            MenuItem('1440p', lambda: on_set_resolution(2560, 1440, 125)),
            MenuItem('1080p', lambda: on_set_resolution(1920, 1080, 100)),
            MenuItem("PS5 Sound", on_listen, lambda item: is_listening),
            MenuItem("Clone/Extend Monitors", on_monitor_change),
            MenuItem('Quit', lambda: on_quit(icon))
        )

        icon.icon = image
        icon.menu = menu
        icon.title = "Resolution Switcher"

        icon.run()
    except Exception as e:
        raise e

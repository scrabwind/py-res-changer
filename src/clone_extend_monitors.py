# import time
#
# import pyautogui
#
# print('Press Ctrl-C to quit.')
# try:
#     while True:
#         x, y = pyautogui.position()
#         positionStr = 'X: ' + str(x).rjust(4) + ' Y: ' + str(y).rjust(4)
#         print(positionStr, end='')
#         time.sleep(0.1)
#         print('\b' * len(positionStr), end='', flush=True)
# except KeyboardInterrupt:
#     print('\n')
from time import sleep

from pyautogui import click


def clone_monitors():
    click(2548, 1413)
    click(1280, 0, button='right')
    click(1374, 300)
    sleep(1)
    click(3946, 118)
    click(4357, 300)
    click(4357, 250)
    sleep(3)
    click(917, 630)


def extend_monitors():
    click(2548, 1413)
    click(1280, 0, button='right')
    click(1374, 365)
    sleep(1)
    click(1708, 384)
    click(2069, 630)
    click(2069, 670)
    sleep(3)
    click(4346, 597)

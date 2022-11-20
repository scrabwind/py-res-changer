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

from pyautogui import click


def clone_monitors():
    click(2548, 1413)
    click(1280, 0, button='right')
    click(1374, 250, interval=1)
    click(3946, 118)
    click(4357, 300)
    click(4357, 250, interval=2)
    click(917, 630, interval=0.25)


def extend_monitors():
    click(2548, 1413)
    click(1280, 0, button='right')
    click(1374, 250, interval=1)
    click(1400, 300)
    click(1800, 500)
    click(1800, 560, interval=2)
    click(3546, 500, interval=0.25)

# Basicly stolen code from:
[Change Windows 10/11 Display Resolution with a Python System Tray Application](https://k0nze.dev/posts/change-resolution-python-system-tray/#:~:text=The%20Python%20code%20for%20changing,a%20file%20called%20resolution_switcher.py%20.)  
I've added change of DPI since I'm using 2560x1440 in 125% scale. Also a way to listen to my monitor as microphone for PS5 audio.


For python code run:

`pyinstaller resolution_changer.spec`

For Go code run:

`go build -ldflags "-H=windowsgui"`

Might add builtin option to run on startup
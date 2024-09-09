import numpy
import sounddevice as sd

assert numpy

is_ps5_connected = True


def callback(indata, outdata, frames, time, status):
    if status:
        print(status)
    outdata[:] = indata


def get_devices(inp: str, out: str):
    formatted_in = inp if "MME" in inp else f"{inp}, MME"
    formatted_out = out if "MME" in out else f"{out}, MME"
    return formatted_out, formatted_in


try:
    default_input = sd.query_devices(kind="output")
    ps5 = sd.query_devices("Monitor - PS5 (High Definition , MME")
    default_output = sd.query_devices(kind="input")
except Exception:
    is_ps5_connected = False
else:
    devices = get_devices(default_input["name"], ps5["name"])

    stream = sd.Stream(device=devices, callback=callback, latency=0.05)


def on_listen_start():
    if not is_ps5_connected:
        return
    if stream.active:
        return
    try:
        stream.start()
    except Exception as e:
        stream.close()
        raise e


def on_listen_stop():
    if not is_ps5_connected:
        return
    if not stream.active:
        return
    try:
        stream.stop()
    except Exception as e:
        stream.abort()
        raise e

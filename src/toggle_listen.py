import numpy
import sounddevice as sd

assert numpy

default_input = sd.query_devices(kind='output')
ps5 = sd.query_devices('Monitor - PS5 (High Definition , MME')
default_output = sd.query_devices(kind='input')


def callback(indata, outdata, frames, time, status):
    if status:
        print(status)
    outdata[:] = indata


def get_devices(inp: str, out: str):
    formatted_in = inp if "MME" in inp else f'{inp}, MME'
    formatted_out = out if "MME" in out else f'{out}, MME'
    return formatted_out, formatted_in


devices = get_devices(default_input['name'], default_output['name'])

stream = sd.Stream(device=devices, callback=callback, latency=0.05)


def on_listen_start():
    if stream.active:
        return
    try:
        stream.start()
    except Exception as e:
        stream.close()
        raise e


def on_listen_stop():
    if not stream.active:
        return
    try:
        stream.stop()
    except Exception as e:
        stream.abort()
        raise e

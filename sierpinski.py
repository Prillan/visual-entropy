#!/usr/bin/python
import pyglet
import random
import sys
import argparse
import math
from bitarray import bitarray
from functools import reduce

from drawing import draw, drawpolygon

CHUNK_SIZE = 1024

def polygon(n):
    return [(
        math.cos((2*h + 1) * math.pi / n),
        math.sin((2*h + 1) * math.pi / n)) for h in range(n)]

def avg(x, y):
    return (x + y) / 2

def file_data(fname):
    f = open(fname, 'rb')
    try:
        while True:
            chunk = f.read(CHUNK_SIZE)
            if len(chunk) > 0:
                yield chunk
            else:
                break
    except:
        pass
    f.close()

def random_data(num_bytes):
    for x in range(num_bytes // CHUNK_SIZE):
        yield bytes(random.randint(0, 255) for i in range(CHUNK_SIZE))

def getcolor(x, n):
    a = int(float(0xFFFFFF)*float(x + 1)/n)
    b = ((a & 0xFF0000) >> 16, (a & 0x00FF00) >> 8, a & 0x0000FF, 255)
    return b

def streamgen(data, n, skip=True):
    bit_buffer = bitarray()
    bits_needed = int(math.ceil(math.log2(n)))

    for chunk in data:
        bit_buffer.frombytes(chunk)
        while len(bit_buffer) >= bits_needed:
            val = bit_buffer[:bits_needed].tobytes()
            bit_buffer = bit_buffer[bits_needed:]
            if val[0] >= n and not skip:
                yield val[0] % n
            elif val[0] < n:
                yield val[0]

def modgen(data, n):
    for chunk in data:
        for b in chunk:
            yield b % n

def pointsgen(data, n, shape):
    current = (0, 0)
    i = 0
    points = []

    for b in data:
        current = (
            avg(current[0], shape[b][0]),
            avg(current[1], shape[b][1])
        )
        i += 1
        points.append(current)
        if i > 10000:
            i = 0
            yield points
            points = []

    yield points

def main():

    parser = argparse.ArgumentParser(
        description="A program for generating fractal patterns using random "
        "or non-random data."
    )

    parser.add_argument("-f", "--file", nargs=1, default="",
                        dest="arg_file", metavar="FILE",
                        help="File to use as binary input."
                        "If no file is given random data will be used.")
    modes = ["stream", "mod", "streammod"]
    parser.add_argument("-m", "--mode", default="mod",
                        metavar="MODE", choices=modes, type=str,
                        help="The mode to use. \n"
                        "  mod - The read byte value is reduced modulus the "
                        "number of edges\n"
                        "  stream - All bits are used in a stream, meaning that"
                        "bytes may overlap. Bytes outside of the interval (0, "
                        "EDGES) will be skipped\n"
                        "  streammod - stream and mod combined.")
    parser.add_argument("-n", nargs=1, default=[20000], dest="arg_num",
                        metavar="BYTES", type=int,
                        help="The number of bytes to use if no file is given.")
    parser.add_argument("-s", "--shape", nargs=1, default=[3],
                        dest="arg_shape", metavar="EDGES", type=int,
                        help="The number of edges in the shape")
    parser.add_argument("--size", nargs=1, default=[512], dest="arg_size",
                        metavar="PIXELS", type=int,
                        help="Size of the window in pixels")
    parser.add_argument("-b", "--block-size", nargs=1, default=[1], type=int,
                        metavar="BYTES", help="Number of bytes to represent "
                        "one point. Bytes are XOR'ed together.")
    parser.add_argument("-d", "--debug", action="store_true", default=False,
                        help="Activate debugging.")

    p = parser.parse_args()

    if len(p.arg_file) > 0 and len(p.arg_file[0]) > 0:
        data = file_data(p.arg_file[0])
    else:
        data = random_data(p.arg_num[0])

    edges = p.arg_shape[0]
    screen_size = p.arg_size[0]

    debug = p.debug

    shape = polygon(edges)
    window = pyglet.window.Window(screen_size + 10, screen_size + 10)

    @window.event
    def on_key_press(s, m):
        if s == pyglet.window.key.ESCAPE:
            pyglet.app.exit()

    window.clear()

    generator = modgen
    if p.mode == "stream":
        generator = streamgen
    elif p.mode == "streammod":
        generator = lambda x, y: streamgen(x, y, skip=False)

    points = pointsgen(generator(data, edges), edges, shape)

    window.set_caption("Not Done!")

    def draw_it(dt):
        try:
            if debug:
                drawpolygon(shape, screen_size)
            current_points = next(points)
            draw(current_points, screen_size)
        except StopIteration:
            window.set_caption("Done!")

    pyglet.clock.schedule_interval(draw_it, 0.1)

    print("Running")
    pyglet.app.run()

if __name__ == "__main__":
    main()



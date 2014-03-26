#!/usr/bin/python
import pyglet
import random
import sys
import argparse
import math
from functools import reduce

from drawing import draw, drawpolygon

def polygon(n):
    return [(
        math.cos((2*h + 1) * math.pi / n),
        math.sin((2*h + 1) * math.pi / n)) for h in range(n)]

def avg(x, y):
    return (x + y) / 2

def file_data(fname, block=1):
    f = open(fname, 'rb')
    try:
        while True:
            c = f.read(block)
            yield reduce(lambda x,y: x ^ ord(y), c, 0)
    except:
        pass
    f.close()

def getcolor(x, n):
    a = int(float(0xFFFFFF)*float(x + 1)/n)
    b = ((a & 0xFF0000) >> 16, (a & 0x00FF00) >> 8, a & 0x0000FF, 255)
    return b

def pointsgen(filedata, r, n, shape):
    current = (0, 0)
    i = 0
    points = []
    for p in filedata:
        xl = r(p, n)
        for x in xl:
            current = (
                avg(current[0], shape[x][0]),
                avg(current[1], shape[x][1])
            )
            i += 1
            points.append(current)
            if i > 10000:
                i = 0
                yield points
                points = []

    yield points

def main():

    def split(x, n):
        for i in range(n):
            if x < (i+1) * (256.0 / n):
                return i

    functions = {
        "mod" : lambda x, y: [x % y],
        "split" : lambda x, y: [split(x, y)]
        }

    parser = argparse.ArgumentParser(
        description="A program for generating fractal patterns using random "
        "or non-random data."
    )

    parser.add_argument("-f", "--file", nargs=1, default="",
                        dest="arg_file", metavar="FILE",
                        help="File to use as binary input."
                        "If no file is given random data will be used.")
    parser.add_argument("-r", "--fun", nargs=1, default="", dest="arg_fun",
                        metavar="FUNCTION", choices=functions,
                        help="The reduction function to use. \n"
                        "Valid choices: %(choices)s")
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

    if len(p.arg_fun) > 0 and p.arg_fun[0] in functions:
        fun = functions[p.arg_fun[0]]
    else:
        fun = lambda x, y: [x % y]

    if len(p.arg_file) > 0 and len(p.arg_file[0]) > 0:
        data = file_data(p.arg_file[0], p.block_size[0])
    else:
        data = (random.randint(0, 255) for i in range(p.arg_num[0]))

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

    points = pointsgen(data, fun, edges, shape)

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



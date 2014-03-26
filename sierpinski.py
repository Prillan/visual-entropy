#!/usr/bin/python
##
##
#
import pyglet
import random
import sys
import argparse
import math
from functools import reduce

SIZE = 500
N = 3
D = [1 , 2]

parser = argparse.ArgumentParser(description="TRIANGLAR FFS!")


triangle = [(0,0), (512,900), (1024,0)]
rectangle = [(0,0), (0, 1024), (1024,0), (1024,1024)]
shape = []

points = []

pointx = lambda n, h: 1 - math.sin((2*h + 1) * math.pi / n)
pointy = lambda n, h: 1 - math.cos((2*h + 1) * math.pi / n)
point = lambda n, h: (
    pointx(n, h),
    pointy(n, h)
    )
pointonscreen = lambda n, h: (
    (SIZE / 2 * pointx(n, h)) + 5,
    (SIZE / 2 * pointy(n, h)) + 5
    )
getpolygon = lambda n: [pointonscreen(n, h) for h in range(n)]

def getglpolygon(n):
    ret = []
    for p in getpolygon(n):
        ret.extend(p)
    return tuple(ret)

def drawpolygon(n):
    points = getglpolygon(n)

    pyglet.graphics.draw(len(points) / 2, pyglet.gl.GL_LINE_LOOP, ('v2f', points), ('c4B', (255, 0, 0, 128) * (len(points)/ 2)))

def draw(points):
    pyglet.graphics.draw(len(points) / 2, pyglet.gl.GL_POINTS, ('v2f', points))#, ("c4B", colors))
    
def halfDist(x, y):
    return int((float(D[0]) * x + y) / D[1])


def fileData(fname, block=1):
    f = open(fname, 'r')
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

# randData : byte list            
def getPoints(filedata, r):
    points = []
    current = (0, 0)
    for p in filedata:
        x = r(p)
        current = (halfDist(current[0], triangle[x][0]), halfDist(current[1], triangle[x][1]))
        #print current
        points.extend(current)
    return tuple(points)

# randData : byte list            
#def drawPoints(filedata, r):
#    print "Hr inne"
#    current = (0, 0)
#    for p in filedata:
#        xl = r(p)
#        for x in xl:
#            current = (halfDist(current[0], triangle[x][0]), halfDist(current[1], triangle[x][1]))
#            i += 1
#            points.extend(current)
#            if i > 1024:
#                yield

def drawPoints(filedata, r, n):
    global points
    current = (SIZE / 2, SIZE / 2)
    i = 0
    for p in filedata:
        xl = r(p, n)
        for x in xl:
            current = (halfDist(current[0], shape[x][0]), halfDist(current[1], shape[x][1]))
            i += 1
            points.extend(current)
            if i > 10000:
                i = 0
                draw(tuple(points))
                points = []
                yield
    draw(tuple(points))

def drawRect(filedata):
    r = lambda x: [x % 4]
    points = []
    current = (0, 0)
    for p in filedata:
        xl = r(p)
        for x in xl:
            current = (halfDist(current[0], rectangle[x][0]), halfDist(current[1], rectangle[x][1]))
            points.extend(current)
    draw(tuple(points))

LIMIT = 0

def main():
    global triangle, shape, SIZE, N, D, LIMIT

    def split(x, n):
        for i in range(n):
            if x < (i+1) * (256.0 / n):
                return i
    
    functions = {
        "mod" : lambda x, y: [x % y],
        "split" : lambda x, y: [split(x, y)]
        #,
        #"baseN" : lambda x, y: [x % 3, (x / 3) % 3, (x / 9) % 3, (x / 27) % 3, (x / 81) % 3]
        }

    parser.add_argument("-f", "--file", nargs=1, default="", dest="arg_file", metavar="FILE", 
                        help="File to use as binary input. If no file is given random data will be used.")
    parser.add_argument("-r", "--fun", nargs=1, default="", dest="arg_fun", metavar="FUNCTION", choices=functions, 
                        help="The reduction function to use. \nValid choices: %(choices)s")
    parser.add_argument("-n", nargs=1, default=[20000], dest="arg_num", metavar="BYTES", type=int,
                        help="The number of bytes to use if no file is given.")
    parser.add_argument("-s", "--shape", nargs=1, default=[3], dest="arg_shape", metavar="EDGES", type=int,
                        help="The number of edges in the shape")
    parser.add_argument("--size", nargs=1, default=[512], dest="arg_size", metavar="PIXELS", type=int,
                        help="Size of the window in pixels")
    parser.add_argument("-b", "--block-size", nargs=1, default=[1], type=int, metavar="BYTES", help="Number of bytes to represent one point. Bytes are XOR'ed together.")
    parser.add_argument("-d", "--dist", nargs=2, default=[1,2], dest="arg_dist", metavar="D E", type=int,
                        help="(X*D + Y) / E = Distance to point")

    p = parser.parse_args(sys.argv[1:])
    
    #print p

    if len(p.arg_fun) > 0 and p.arg_fun[0] in functions:
        fun = functions[p.arg_fun[0]]
    else:
        fun = lambda x, y: [x % y]

    if len(p.arg_file) > 0 and len(p.arg_file[0]) > 0:
        data = fileData(p.arg_file[0], p.block_size[0])
    else:

        LIMIT = p.arg_num[0]
        data = (random.randint(0, 255) for i in range(LIMIT))
    
    N = p.arg_shape[0]
    SIZE = p.arg_size[0]
    D = p.arg_dist

    shape = getpolygon(N)
    window = pyglet.window.Window(SIZE + 10, SIZE + 10)    
    
    @window.event
    def on_draw():
        #global points
        #draw(getPoints(data, fun))
#        drawpolygon(N)
 #       drawPoints(data, fun, N)
        #drawRect(data)
        #draw(tuple(points))
        points = []
        #pass

    @window.event
    def on_key_press(s, m):
        if s == pyglet.window.key.ESCAPE:
            pyglet.app.exit()
        
    window.clear()

    draw_gen = drawPoints(data, fun, N)

    window.set_caption("Not Done!")

    def draw_it(dt):
        try:
            next(draw_gen)
        except StopIteration:
            window.set_caption("Done!")

    pyglet.clock.schedule_interval(draw_it, 0.1)

    print("Running")
    pyglet.app.run()

if __name__ == "__main__":
    main()



#!/usr/bin/python
import sys
import argparse
import struct
import math
import os
import matplotlib.pyplot as plt


parser = argparse.ArgumentParser()


parser.add_argument('-p', '--pieces', nargs=1, default=[1], dest="pieces", metavar="PIECES", help="Break down file into pieces", type=int)
parser.add_argument('-b', '--block-size', nargs=1, default=[1], metavar="BLOCKSIZE", type=int, help="Number of bytes in a 'block'")
parser.add_argument('-x', '--x-data', nargs=1, choices=["byte", "percent"], default=["byte"], help="Set x-axis to display either byte or percent")
parser.add_argument('--plot', action='store_true', help="Plot entropies after finished calculating them")
parser.add_argument('-f', '--file', nargs='+', required=True)

def byte(c):
    return struct.unpack("B", c)[0]
def bytel(cl):
    s = 0
    for i in range(len(cl)):
        s += byte(cl[i]) << (8 * (len(cl) - 1 - i))
    return s

def freqentropy(f, blocksize, maxbytes=0):
    freq_list = {}
    
    count = int(0)

    while True:
        temp = f.read(blocksize)
        if not len(temp) == blocksize:
            break # EOF
        bl = bytel(temp)
        if not bl in freq_list:
            freq_list[bl] = 1
        else:
            freq_list[bl] += 1
        count += 1
        if (not maxbytes == 0) and (count*blocksize >= maxbytes):
            break
    e = 0

    if count == 0:
        print f, blocksize, maxbytes

    T1 = 1 / float(count)
    lTT1 = math.log(count, 256 ** blocksize) * T1
    
    for x in freq_list:
        i = freq_list[x]
        if not i == 0:
            e -= math.log(i, 256 ** blocksize) * i * T1 - lTT1 * i

    return e


def main():
    args = parser.parse_args()
    
    print args

    elist = []

    for fn in args.file:

        size = os.path.getsize(fn)

        f = open(fn, 'r')
    
        e = []

        maxbytes = float(size) / float(args.pieces[0])
        
        print "byte,entropy" if not args.x_data[0] == "percent" else "percent,entropy"
    
        for i in range(args.pieces[0]):
            maxbyte = ((i + 1) * maxbytes)
            e.append((int(maxbyte), freqentropy(f, args.block_size[0], int(maxbytes))))
            if args.x_data[0] == "percent":
                e[len(e) - 1] = (e[len(e) - 1][0] / float(size), e[len(e) - 1][1])
            print str(e[len(e) - 1][0]) + "," + str(e[len(e) - 1][1])

        elist.append(e)

        f.close()    

    if args.plot:
        for i in range(len(args.file)):
            plt.plot([x[0] for x in elist[i]], [x[1] for x in elist[i]], label=args.file[0])
        plt.legend(tuple(args.file), loc='best')
        plt.draw()
        plt.show()

if __name__ == "__main__":
    main()

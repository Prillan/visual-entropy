import pyglet
import argparse
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser()

parser.add_argument('-f', '--file', required=True, nargs='+', metavar="FILE")
parser.add_argument('-s', '--separator', nargs=1, default=[","], metavar="CHAR")

parser.add_argument('-x', '--x-label', nargs=1, default=[""], metavar="TEXT")
parser.add_argument('-y', '--y-label', nargs=1, default=[""], metavar="TEXT")

SIZE = 500


def main():

    args = parser.parse_args()

    sep = args.separator[0]

    lines = []

    for fn in args.file:
        f = open(fn, 'r')

        labels = f.readline().strip().split(sep)

        if len(args.x_label[0]) > 0:
            xlabel = args.x_label[0]
        else:
            xlabel = labels[0]
        if len(args.y_label[0]) > 0:
            ylabel = args.y_label[0]
        else:
            ylabel = labels[1]

        l = [x.split(sep) for x in f]
        lines.append(l)
        
        plt.plot([x[0] for x in l], [x[1] for x in l], label=fn)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)

    plt.legend(tuple(args.file), loc='best')
    plt.draw()
    plt.show()


main()

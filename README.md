## Visual Entropy ##

Scripts for visualizing the amount of information in files.

### sierpinski.py ###

Generates generalized Sierpinski regular n-gons using the simple process
below:

1. Inscribe a regular n-gon in the unit circle and label the vertices
   counter-clockwise 0, 1, ..., n.
2. Start at the point (0, 0)
3. Draw a dot at the current point
4. Get a random value in the interval [0, n-1].
5. Our new point is halfway to the vertex with the label corresponding
   to the above random value above.
6. Repeat 3-5

#### Usage ####

    usage: sierpinski.py [-h] [-f FILE] [-m MODE] [-n BYTES] [-s EDGES]
                         [--size PIXELS] [-d]
    
    A program for generating fractal patterns using random or non-random data.
    
    optional arguments:
      -h, --help            show this help message and exit
      -f FILE, --file FILE  File to use as binary input.If no file is given random
                            data will be used.
      -m MODE, --mode MODE  The mode to use. mod - The read byte value is reduced
                            modulus the number of edges stream - All bits are used
                            in a stream, meaning thatbytes may overlap. Bytes
                            outside of the interval (0, EDGES) will be skipped
                            streammod - stream and mod combined.
      -n BYTES              The number of bytes to use if no file is given.
      -s EDGES, --shape EDGES
                            The number of edges in the shape
      --size PIXELS         Size of the window in pixels
      -d, --debug           Activate debugging.

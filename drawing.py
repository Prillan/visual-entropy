import pyglet

# Points should be inside or on the unit circle.
def _point_to_screen(point, screen_size):
    return (
        (screen_size / 2) * (1 - point[0]) + 5,
        (screen_size / 2) * (1 + point[1]) + 5
    )
def _points_to_screen_tuple(points, screen_size):
    return tuple(x for p in points
                 for x in _point_to_screen(p, screen_size))

def draw(points, screen_size):
    gl_points = _points_to_screen_tuple(points, screen_size)

    pyglet.graphics.draw(
        len(points),
        pyglet.gl.GL_POINTS,
        ('v2f', gl_points)
    )#, ("c4B", colors))

def drawpolygon(polygon, screen_size):
    points = _points_to_screen_tuple(polygon, screen_size)

    pyglet.graphics.draw(
        len(points) // 2,
        pyglet.gl.GL_LINE_LOOP,
        ('v2f', points),
        ('c4B', (255, 0, 0, 128) * (len(points) // 2))
    )

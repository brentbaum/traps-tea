from stibble import stibble
from PIL import Image, ImageDraw
import sys


def draw_lines(points, img):
    out = img.point(lambda i: 255)
    d = ImageDraw.Draw(out)

    for i in range(len(points) - 1):
        d.line([points[i], points[i + 1]], fill=128)

    del d

    return out

def draw_points(positions, out):
    draw = ImageDraw.Draw(out)

    for (x, y) in positions:
        draw.ellipse((x - 2, y - 2, x + 2, y + 2), fill=0)
    del draw

    out.show()

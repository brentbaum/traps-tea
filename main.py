from stibble import stibble
from draw import draw_lines
from PIL import Image, ImageDraw
from tsp import nearestNeighbor
import sys

def make_art(filename, n_points):
    img = Image.open(filename).convert('LA')

    points = stibble(img, n_points)
    ordered = nearestNeighbor(points)

    out = draw_lines(ordered, img)
    out.show()

if __name__ == "__main__":
    n_points = int(sys.argv[2])
    filename = sys.argv[1]
    make_art(filename, n_points)

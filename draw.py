from stibble import stibble
from PIL import Image, ImageDraw
import sys


def draw_lines(points, out):
    d = ImageDraw.Draw(out)

    for i in range(len(points) - 1):
        d.line([points[i], points[i + 1]], fill=128)

    del d

    out.show()

if __name__ == "__main__":
    filename = sys.argv[1]
    img = Image.open(filename).convert('LA')
    points = stibble(img, 100)
    draw_lines(points, img.point(lambda i: 255)) 

    print(sorted(points))
    

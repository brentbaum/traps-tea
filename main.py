from stibble import stibble
from draw import draw_lines
from PIL import Image, ImageDraw
from tsp import nearestNeighbor, just_solve_it
import sys
import time

def resize(img):
    basewidth = 150
    wpercent = (basewidth/float(img.size[0]))
    hsize = int((float(img.size[1])*float(wpercent)))
    return img.resize((basewidth,hsize), Image.ANTIALIAS)

def make_art(filename, n_points):
    img = Image.open(filename).convert('LA')
    img = resize(img)

    points = stibble(img, n_points)
    tour = just_solve_it(points)
    
    out = draw_lines(tour, img)
    out.show()

if __name__ == "__main__":
    n_points = int(sys.argv[2])
    filename = sys.argv[1]

    start_time = int(round(time.time() * 1000))
    make_art(filename, n_points)
    end_time = int(round(time.time() * 1000))
    print(end_time - start_time, "milliseconds")

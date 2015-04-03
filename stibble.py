from __future__ import division
from PIL import Image, ImageDraw
import sys
from random import random, choice
import math

def draw(positions, out):
    draw = ImageDraw.Draw(out)

    for (x, y) in positions:
        draw.ellipse((x - 2, y - 2, x + 2, y + 2), fill=0)
    del draw

    out.show()

def histogram(img):
    hist = map(lambda l: [], range(256))
    for x in range(img.size[0]):
        for y in range(img.size[1]):
            hist[img.getpixel((x, y))[0]].append((x, y))
    return hist

def weighted_histogram(img):
    hist = histogram(img)
    whist = []
    previous = -1
    for i in range(0, len(hist)):
        lower = previous + 1
        upper = previous = lower + len(hist[i]) * (255 - i)
        whist.append(((lower, upper), hist[i]))
    return whist

def stibble(img, n_points, should_draw=False):
    positions = list()

    hist = weighted_histogram(img)
    upper = hist[-1][0][1]

    for p in range(0, n_points):
        X = math.floor(random() * upper)
        b = next(bin for bin in hist if X >= bin[0][0] and X <= bin[0][1])[1]
        positions.append(choice(b))

    if should_draw:
        draw(positions, img.point(lambda i: 255))
    
    return positions

if __name__ == "__main__":
    if len(sys.argv) is 3:
        n_points = int(sys.argv[2])
        filename = sys.argv[1]
        img = Image.open(filename).convert('LA')
        stibble(img, n_points)
    else:
        print "Incorrect number of arguments."

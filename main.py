from stibble import stibble
from draw import draw_lines
from PIL import Image, ImageDraw
from tsp import nearestNeighbor, twoOptSwap, swap_intersect#, just_solve_it
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

    #tour = just_solve_it(points)
    ordered = nearestNeighbor(points)

    twoopt_ordered = twoOptSwap(ordered)
    swap_ordered = swap_intersect(ordered)
    
    ordered += [ordered[0]] 
    twoopt_ordered += [twoopt_ordered[0]]
    swap_ordered += [swap_ordered[0]]
	
    out = draw_lines(ordered, img)
    out.save("output.png")
    out2 = draw_lines(twoopt_ordered, img)
    out2.save("twooptout.png")
    out3 = draw_lines(swap_ordered, img)
    out3.save("swapout.png")
    #out4 = draw_lines(tour, img)
    #out4.save("justsolveit.png")

if __name__ == "__main__":
    n_points = int(sys.argv[2])
    filename = sys.argv[1]
    start_time = int(round(time.time() * 1000))
    make_art(filename, n_points)
    end_time = int(round(time.time() * 1000))
    print(end_time - start_time, "milliseconds")

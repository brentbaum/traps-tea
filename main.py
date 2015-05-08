from stibble import stibble
from draw import draw_lines, draw_mst
from PIL import Image, ImageDraw
from tsp import nearestNeighbor, twoOptSwap, swap_intersect, mst_to_path, mst_tour_2, advancedNearestNeighbor#, just_solve_it
import sys
import time

def resize(img):
    basewidth = 400
    wpercent = (basewidth/float(img.size[0]))
    hsize = int((float(img.size[1])*float(wpercent)))
    return img.resize((basewidth,hsize), Image.ANTIALIAS)


def make_art(filename, n_points):
    img = Image.open(filename).convert('LA')
    img = resize(img)
	
    file_suffix = str(n_points) + ".png"
    
    print("Stippling....")
    points = stibble(img, n_points)
    print("Nearest Neighbor....")
    ordered = nearestNeighbor(points)
    print("MST....")
    mst = mst_tour_2(points)
    out5 = draw_mst(mst, img)
    out5.save("out/mst.png")
    print("Converting to tour....")
    tour = mst_to_path(mst)
    print("Swap Intersects....")
    swap_ordered = swap_intersect(tour[:len(tour)-1])
    
    ordered += [ordered[0]] 
    swap_ordered += [swap_ordered[0]]
       
    print("Saving....")	
    out = draw_lines(ordered, img)
    out.save("out/nn.png")
    #out2 = draw_lines(twoopt_ordered, img)
    #out2.save("out/twooptout.png")
    out3 = draw_lines(swap_ordered, img)
    out3.save("out/swapopt.png")
    #out4 = draw_lines(tour, img)
    #out4.save("justsolveit.png")
    
    out6 = draw_lines(tour, img)
    out6.save("out/mst_path.png")
	 
    print("Done!")
    print("nn.png: nearest neighbor, no optimizations")
    print("mst.png: mst")
    print("mst_path.png: mst to path, no optimizations")
    print("swapopt.png: mst to path, intersection optimization run")

if __name__ == "__main__":
    n_points = int(sys.argv[2])
    filename = sys.argv[1]
    start_time = int(round(time.time() * 1000))
    make_art(filename, n_points)
    end_time = int(round(time.time() * 1000))
    print(end_time - start_time, "milliseconds")

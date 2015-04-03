import math
import sys
import stibble
import heapq
import time

def readFromFile():
	text_file = open("test.txt", "r")
	lines = text_file.read().split('\n')
	text_file.close()
	pointList = []
	for each in lines:
		if each != "":
			point = each.split(',')
			xval = int(point[0][1:])
			yval = int(point[1][:(len(point[1])-1)])
			pointList += [(xval, yval)]
	return pointList

def distance(p1, p2):
	return math.sqrt((p1[0]-p2[0])*(p1[0]-p2[0]) + (p1[1]-p2[1])*(p1[1]-p2[1]))

def tour_length(points):
        dist = 0
        for i in range(len(points)):
                dist += distance(points[i], points[(i + 1) % len(points)])
        return dist

def connects(edge, mst):
    source, dest, _ = edge

    for s, d, _ in mst:
        if source == s or source == d or \
           dest == s or dest == d:
            return True

    return False

def min_connecting_edge(mst, edges):
    min_edge = None
    for edge in edges:
           if connects(edge, mst) \
              and (not min_edge or edge[2] < min_edge[2]):
            min_edge = edge
    return min_edge

def mst_tour(points):
        mst = []
        edges = []
        print_time()
        for v in points:
                for w in points:
                        if v is not w:
                                edges.append((v, w, distance(v, w)))
        print_time()

        if not edges:
                return mst

        mst = [edges.pop()]

        while len(mst) < len(points) - 1:
                min_edge = min_connecting_edge(mst, edges)
                edges.remove(min_edge)
                mst.append(min_edge)
        print_time()

def nearestNeighbor(pointList):
	uList = [pointList[0]]
	vList = pointList[1:]
	while len(vList) != 0:
		u = uList[len(uList)-1]
		minDist = distance(u, vList[0])
		addV = vList[0]
		for each in vList:
			newDist = distance(u, each)
			if newDist < minDist:
				minDist = newDist
				addV = each
		uList += [addV]
		vList.remove(addV)
        print(tour_length(uList))
	return uList	

def clarkWright(pointList):
	return pointList	

def twoOptSwap(pointList):
	tour = pointList
	currDist = distance(tour[0], tour[len(tour)-1])
	for i in range(len(tour)-1):
		currDist += distance(tour[i], tour[i+1])
	changed = True
	while(changed):
		changed = False
		for i in range(len(tour)-1):
			pointA1 = tour[i]
			pointA2 = tour[i+1]
			for k in range(i+1, len(tour)-1):
				pointB1 = tour[k]
				pointB2 = tour[k+1]
				originalLength = distance(pointA1, pointA2) + distance(pointB1, pointB2) 
				testLength = distance(pointA1, pointB2) + distance(pointA2, pointB1)
				if testLength < originalLength:
					currDist = currDist - originalLength + testLength 
					print currDist
					tour = tour[:i+1] + [tour[k+1]] + tour[i+2:k+1] + [tour[i+1]] + tour[k+2:]

					changed = True
					break

def main(pointList):	
	nearestNeighborOrder = nearestNeighbor(pointList)
	#optSwapTour = twoOptSwap(nearestNeighborOrder)
	#print optSwapTour	
	#clarkWrightOrder = clarkWright(pointList)


if __name__ == "__main__":
	if len(sys.argv) is 3:
		n_points = int(sys.argv[2])
		img = Image.open(sys.argv[1]).convert('LA')
		pointList = stibble(img)	
		main(pointList)
	else:
		print "Incorrect number of arguments"

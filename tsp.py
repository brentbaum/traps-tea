import math
import sys
import stibble
import heapq

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

def mst(pointList):
	segments = []
	for i in range(len(pointList)):
		for j in range(i+1, len(pointList)):
			#segments is a list of a 3-ple: (point1, point2, distance)
			segments += [(pointList[i], pointList[j], distance(pointList[i], pointList[j]))]
	sortedSegments = sorted(segments, key=lambda each:each[2])

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

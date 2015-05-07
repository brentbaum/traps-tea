import math
import sys
import stibble
import heapq
import time
from PIL import Image


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
	return (p1[0]-p2[0])*(p1[0]-p2[0]) + (p1[1]-p2[1])*(p1[1]-p2[1])

def tour_length(points):
        dist = 0
        for i in range(len(points)):
                dist += distance(points[i], points[(i + 1) % len(points)])
        return dist


def adjacent(mst, p):
	adj_list = []
	to_remove = []
	for (p1, p2, d) in mst:
		if(p1 == p):
			adj_list.append((p1, p2, d))
			to_remove += [(p1, p2, d)]
		elif(p2 == p):
			adj_list.append((p2, p1, d))
			to_remove += [(p1, p2, d)]
	for each in to_remove:
		mst.remove(each)
	return adj_list

def ham_path(mst):
	path = [mst[0][0], mst[0][1]]
	index = 1
	last = path[-1]
	while(len(path) < len(mst)):
		print("len path: " + str(len(path)))
		adj = adjacent(mst, last)
		adj = sorted([node for node in adj if node[0] not in path], key=lambda node: node[1])
		if(len(adj) > 0):
			path.append(adj[0][0])
			index = -1
		else:
			index -= 1
			last = path[index]
	path.append(path[0])
	return path	

def mst_to_path(mst):
	path = []
	start_point = mst[0][0]
	path += [start_point]
	adj_list = adjacent(mst, start_point)
	while len(adj_list) > 0:
		next_edge = adj_list.pop()
		path += [next_edge[1]]
		to_add = adjacent(mst, next_edge[1])
		to_add = sorted(to_add, key=lambda edge: edge[1][0])
		adj_list += to_add
	path.append(path[0])	
	return path
	

def connects_to_unknown(edge, known):
    s, d, _ = edge
    if (s in known and d not in known) or (d in known and s not in known):
            return True
    return False

def min_connecting_edge(mst, edges, known):
	min_edge = edges[0]
	to_remove = []
	for edge in edges:
		if (edge[0] in known and edge[1] in known):
			to_remove += [edge]
		elif connects_to_unknown(edge, known) and edge[2] < min_edge[2]:
			min_edge = edge
	for each in to_remove:
		edges.remove(each)
	return min_edge

def build_adj(points):
	adjacency_matrix = dict()
	for v in points:
		for w in points:
			adj_dist = distance(v, w)
			adjacency_matrix[(v, w)] = adj_dist
			adjacency_matrix[(w, v)] = adj_dist
	return adjacency_matrix

def mst_tour(points):
	mst = []
	known = {}
	edges = []
	
	for i in range(len(points)):
		for j in range(i+1, len(points)):
			edges.append((points[i], points[j], distance(points[i], points[j])))
	edges.sort(key=lambda e: e[2], reverse=True)
	
	mst = [edges.pop()]
	known = set()
	known.add(mst[0][0])
	known.add(mst[0][1])
	while len(mst) < len(points) - 1:
		min_edge = min_connecting_edge(mst, edges, known)
		edges.remove(min_edge)
		mst.append(min_edge)
		known.add(min_edge[0])
		known.add(min_edge[1])
	return mst #ham_path(mst)

def mst_tour_2(points):
	mst = []
	known = []

	adj_matrix = build_adj(points)
	
	known += [points.pop()]
	while(len(points) > 0):
		min_edge = (known[0], points[0], adj_matrix[(known[0], points[0])])
		for each_known in known:
			for each_unknown in points:
				new_dist = adj_matrix[(each_known, each_unknown)]
				if new_dist < min_edge[2]:
					min_edge = (each_known, each_unknown, new_dist)
		mst.append(min_edge)
		known += [min_edge[1]]
		points.remove(min_edge[1])
		#print("known: " + str(len(known)))
		#print("unknown: " + str(len(points)))
	return mst

def nn_intersect_check(segment, point_list):
	for i in range(len(point_list)-1):
		check_segment = (point_list[i], point_list[i+1])
		if calc_intersect(segment, check_segment):
			return True
	return False

def nearestNeighbor(pointList):
	uList = [pointList[0]]
	vList = pointList[1:]
	while len(vList) != 0:
		u = uList[len(uList)-1]
		minDist = distance(u, vList[0])
		addV = vList[0]
		for each in vList:
			newSegment = (u, each, distance(u, each))
			if newSegment[2] < minDist and not (nn_intersect_check(newSegment, uList)):
				minDist = newSegment[2] 
				addV = each
		uList += [addV]
		vList.remove(addV)
	return uList

def advancedNearestNeighbor(pointList):
	edges = []
	for i in range(len(pointList)):
		for j in range(i+1, len(pointList)):
			edges += [(pointList[i], pointList[j], distance(pointList[i], pointList[j]))]
	edges.sort(key=lambda a: a[2])
	print(edges[0][2])
	print(edges[10][2])
	

def calc_intersect(line1, line2):
	if line1[0][0] == line1[1][0] or line2[0][0] == line2[1][0]:
		return False
	slope1 = (line1[0][1] - line1[1][1]) / (line1[0][0] - line1[1][0]) 
	slope2 = (line2[0][1] - line2[1][1]) / (line2[0][0] - line2[1][0]) 
	if slope1 == slope2:
		return False
	b1 = line1[0][1] - (slope1 * line1[0][0])
	b2 = line2[0][1] - (slope2 * line2[0][0])
	x_int = (b2 - b1) / (slope1 - slope2)
	if (line1[0][0] < x_int and x_int < line1[1][0]) or (line1[1][0] < x_int and x_int < line1[0][0]):
		return True
	return False


def swap_intersect(point_list):
	tour = point_list
	curr_dist = distance(tour[0], tour[len(tour)-1])
	for i in range(len(tour)-1):
		curr_dist += distance(tour[i], tour[i+1])
	#print("initial: " + str(curr_dist))
	changed = True
	#for times in range(20):
	while(changed):
		changed = False
		for i in range(len(tour)-1):
			for k in range(i+2, len(tour)-1):
				line1 = (tour[i], tour[i+1])
				line2 = (tour[k], tour[k+1])
				
				if calc_intersect(line1, line2):
					segment = tour[i+1:k+1]
					segment.reverse() 
					new_tour = tour[:i+1] + segment + tour[k+1:]

					subtract_dist = distance(tour[i], tour[i+1]) + distance(tour[k], tour[k+1])
					add_dist = distance(tour[i], tour[k]) + distance(tour[i+1], tour[k+1])
					
					new_dist = curr_dist - subtract_dist + add_dist
					if new_dist < curr_dist:
						tour = new_tour
						curr_dist = new_dist
						#print(curr_dist)
						changed = True
						break
			if changed:
				break
	print("Final Length: " + str(curr_dist))
	return tour 


def twoOptSwap(pointList):
	tour = pointList
	currDist = distance(tour[0], tour[len(tour)-1])
	for i in range(len(tour)-1):
		currDist += distance(tour[i], tour[i+1])
	changed = True
	for times in range(50):
	#while(changed):
		changed = False
		for i in range(len(tour)):
			for k in range(i+1, len(tour)):
				segment = tour[i:k+1]
				segment.reverse()
				new_tour = tour[:i] + segment + tour[k+1:]
				new_dist = distance(new_tour[0], new_tour[len(new_tour)-1])
				for index in range(len(new_tour)-1):
					new_dist += distance(new_tour[index], new_tour[index+1]) 
				if new_dist < currDist: 
					currDist = new_dist
					tour = new_tour
					print(currDist)
					changed = True
					break
			if changed:
				break
	print("final: " + str(currDist))
	return tour


def main(pointList):	
	print("Nearest Neighbor....")
	nearestNeighborOrder = nearestNeighbor(pointList)
	print("Opt Swap Tour....")
	optSwapTour = twoOptSwap(nearestNeighborOrder)
	print(optSwapTour)


if __name__ == "__main__":
	if len(sys.argv) is 3:
		n_points = int(sys.argv[2])
		img = Image.open(sys.argv[1]).convert('LA')
		print("Stippling....")
		pointList = stibble.stibble(img, n_points)	
		main(pointList)
	else:
		print("Incorrect number of arguments")

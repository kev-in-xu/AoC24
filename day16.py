import re
import numpy as np
import itertools
import math
import copy
import heapq
from collections import deque, Counter

test = False
day = "16" # map puzzle Dijkstra's

if test:
    filename = f"day{day}-input-test.txt"
else:
    filename = f"day{day}-input.txt"

# input parsing
with open(filename, "r") as file:
    lines = [l.strip() for l in file]

    arr = []
    visitedArr = []
    for row in lines:
        row = [c for c in row]
        visitedRow = [0 for _ in row]
        arr.append(row)
        visitedArr.append(visitedRow)

bestPathArr = copy.deepcopy(visitedArr)
partTwoArr = copy.deepcopy(visitedArr)

def printMap(arr):
    for row in arr:
        print("".join([str(n) for n in row]))

def OOB(y, x, arr): # check out of bounds
    return y < 0 or y >= len(arr) or x < 0 or x >= len(arr[0])

def findChar(arr, char):
    for i in range(len(arr)):
        for j in range(len(arr[0])):
            if arr[i][j] == char:
                return i, j

#printMap(arr)
#print(findChar(arr, 'S'))


#print(coord)

# 0 up | 1 right | 2 down | 3 left
dirs = [(-1,0), (0,1), (1,0), (0,-1)]

# cost, coord, direction
def findBestPath(arr):
    coord = findChar(arr, 'S')
    toVisit = [(0, coord, 1, 0)]
    visited = set()

    heapq.heapify(toVisit)

    while toVisit:
        currCost, currCoord, currDir, steps = heapq.heappop(toVisit)
        y, x = currCoord
        #print(currCost, currCoord, currDir, arr[y][x])

        if (y, x) in visited:
                continue

        if arr[y][x] == 'E':
            return currCost

        # iterate through directions
        visits = 0
        for i in range(len(dirs)):
            dY, dX = dirs[i]
            newY, newX = y + dY, x + dX
            
            if arr[newY][newX] == '#':
                continue

            visits += 1
            if i == currDir:
                heapq.heappush(toVisit, (currCost + 1, (newY, newX), i, steps+1))
            else:
                heapq.heappush(toVisit, (currCost + 1001, (newY, newX), i, steps+1))
        
        visitedArr[y][x] += 1
        
        if visitedArr[y][x] == visits:
            visited.add(currCoord)


bestCost = findBestPath(arr)
print("part 1:", bestCost)

def findAllPaths(arr, bestCost):
    coord = findChar(arr, 'S')
    visited = []
    toVisit = [(0, coord, 1, 0, visited)]

    heapq.heapify(toVisit)
    validPaths = []

    while toVisit:
        currCost, currCoord, currDir, steps, prevs = heapq.heappop(toVisit)
        y, x = currCoord
        #print(currCost, currCoord, currDir, arr[y][x], steps)
        
        if bestPathArr[y][x] != 0 and currCost > bestPathArr[y][x]:
            #print('visited before but more inefficiently')
            continue

        if currCost == bestCost and arr[y][x] == 'E':
            validPaths.append(prevs)
            #print(prevs)
            #print("found a path!")

        # iterate through directions
        paths = 0
        for i in range(len(dirs)):
            dY, dX = dirs[i]
            newY, newX = y + dY, x + dX
            
            if arr[newY][newX] == '#':
                continue

            paths += 1

            # don't backtrack
            if (i + 2) % 4 == currDir:
                continue
            
            # allows going straight or turning
            prevs.append(currCoord)
            newPrevs = copy.copy(prevs)
            if i == currDir:
                heapq.heappush(toVisit, (currCost + 1, (newY, newX), i, steps+1, newPrevs))
            else:
                heapq.heappush(toVisit, (currCost + 1001, (newY, newX), i, steps+1, newPrevs))
        
        if paths == 2:
            bestPathArr[y][x] = currCost
        
        # if it's on a straight path, and there are no crossroads, and currCost is greater than maxCost of the location, drop it
    return validPaths

validPaths = findAllPaths(arr, bestCost)

for path in validPaths:
    for coord in path:
        y, x = coord
        partTwoArr[y][x] = 1

#printMap(partTwoArr)

res = sum([row.count(1) for row in partTwoArr])
print("part 2:", res)
"""
use heap to keep track of next nodes to explores along with total cost of being in that step

"""


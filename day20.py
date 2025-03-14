import re
import numpy as np
import itertools
import math
import copy
import heapq
import time
from collections import deque, Counter

test = False
day = "20"

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
        visitedRow = [c for c in row]
        arr.append(row)
        visitedArr.append(visitedRow)
    

def printMap(arr):
    for row in arr:
        print("".join([str(n) for n in row]))

def OOB(y, x, arr): # check out of bounds
    return y < 0 or y >= len(arr) or x < 0 or x >= len(arr[0])

def makeNewArr(size):
    arr = []
    for _ in range(size):
        row = [0] * size
        arr.append(row)
    return arr

def plotBytes(bytes, size):
    arr = makeNewArr(size)

    for coord in lines[:bytes]:
        x, y = coord
        arr[y][x] = '#'
    return arr

def findChar(arr, char):
    for i in range(len(arr)):
        for j in range(len(arr[0])):
            if arr[i][j] == char:
                return i, j

dirs = [(-1,0), (0,1), (1,0), (0,-1)]

#printMap(arr)

# use pathfinder from earlier to mark out steps in the array
def findBestPath(arr):
    sY, sX = findChar(arr, 'S')
    eY, eX = findChar(arr, 'E')
    toVisit = [(0,(sY,sX))]

    heapq.heapify(toVisit)
    visitedArr = makeNewArr(len(arr))
    firstStepArr = makeNewArr(len(arr))
    coordPath = []

    while toVisit:
        steps, currCoord = heapq.heappop(toVisit)
        y, x = currCoord
        #print(currCoord, steps)
        #print(currCost, currCoord, currDir, arr[y][x])

        if visitedArr[y][x] == 1:
            continue

        if y == eY and x == eX:
            #print("reached end")
            #printMap(firstStepArr)
            firstStepArr[y][x] = steps
            coordPath.append((y,x))
            return steps, coordPath, firstStepArr

        # iterate through directions
        for i in range(len(dirs)):
            dY, dX = dirs[i]
            newY, newX = y + dY, x + dX
            #print(newY, newX)
            
            if OOB(newY, newX, arr) or arr[newY][newX] == '#':
                continue
            #print("pushing")
            heapq.heappush(toVisit, (steps + 1, (newY, newX)))
        
        firstStepArr[y][x] = steps
        coordPath.append((y,x))
        visitedArr[y][x] = 1
    
    # if couldn't find the end
    
    return None

steps, coords, firstStepArr = findBestPath(arr)
#print(steps)

#printMap(firstStepArr)

def getNeighbors(dist):
    neighbors = []
    dirs = [(1,1), (1,-1), (-1,1), (-1,-1)]
    for i in range(1, dist+1):
        for j in range(i+1):
            dY, dX = j, i-j
            for dir in dirs:
                neighbors.append((dY * dir[0], dX * dir[1], i)) # dY, dX, cheatLength
    return neighbors

def checkCheats(firstStepArr, y, x, dist):

    steps = firstStepArr[y][x]
    neighbors = getNeighbors(dist)

    cheats = set()
    for neighbor in neighbors: # neighbor = (dY, dX, cheatLength)
        newY, newX = y + neighbor[0], x + neighbor[1]
        if not OOB(newY, newX, firstStepArr):
            if firstStepArr[newY][newX] != 0 and (firstStepArr[newY][newX] - steps) >= 100 + neighbor[2]: # add cheatLength to steps needed
                cheats.add(((y, x), (newY, newX)))
    return list(cheats)



print("part 1:", sum([len(checkCheats(firstStepArr, coord[0], coord[1], 2)) for coord in coords]))

print("part 2:", sum([len(checkCheats(firstStepArr, coord[0], coord[1], 20)) for coord in coords]))       


# more readable version of print statements below
"""
total = 0
for coord in coords:
    y, x = coord

    result = checkCheats(firstStepArr, y, x, 2)
    total += len(result)

print(total)"""

"""total = 0
for coord in coords:
    y, x = coord

    result = checkCheats(firstStepArr, y, x, 20)
    total += len(result)

print(total)"""
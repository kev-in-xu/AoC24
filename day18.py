import re
import numpy as np
import itertools
import math
import copy
import heapq
import time
from collections import deque, Counter

test = False
day = "18" # map puzzle BFS

if test:
    filename = f"day{day}-input-test.txt"
else:
    filename = f"day{day}-input.txt"

# input parsing
with open(filename, "r") as file:
    lines = [(int(l.strip().split(',')[0]), int(l.strip().split(',')[1])) for l in file]

def printMap(arr):
    for row in arr:
        print("".join([str(n) for n in row]))

def OOB(y, x, arr): # check out of bounds
    return y < 0 or y >= len(arr) or x < 0 or x >= len(arr[0])

def makeNewArr(size):
    arr = []
    for _ in range(size):
        row = ['.'] * size
        arr.append(row)
    return arr

def plotBytes(bytes, size):
    arr = makeNewArr(size)

    for coord in lines[:bytes]:
        x, y = coord
        arr[y][x] = '#'
    return arr


arr = plotBytes(1024, 71)
#printMap(arr)
#print(lines)

# 0 up | 1 right | 2 down | 3 left
dirs = [(-1,0), (0,1), (1,0), (0,-1)]

# cost, coord, direction

visitedArr = []
def findBestPath(arr):
    toVisit = [(0,(0,0))]

    heapq.heapify(toVisit)
    visitedArr = makeNewArr(len(arr))

    while toVisit:
        steps, currCoord = heapq.heappop(toVisit)
        y, x = currCoord
        #print(currCoord, steps)

        #print(currCost, currCoord, currDir, arr[y][x])

        if visitedArr[y][x] == 1:
            continue

        if y == len(arr)-1 and x == len(arr[0])-1:
            #print("reached end")
            return steps

        # iterate through directions
        for i in range(len(dirs)):
            dY, dX = dirs[i]
            newY, newX = y + dY, x + dX
            #print(newY, newX)
            
            if OOB(newY, newX, arr) or arr[newY][newX] == '#':
                #print("oob")
                continue
            #print("pushing")
            heapq.heappush(toVisit, (steps + 1, (newY, newX)))
        
        visitedArr[y][x] = 1
    
    # if couldn't find the end
    return None
    

print("part 1:", findBestPath(arr))
#printMap(arr)
#printMap(visitedArr)
#print("part 2")


start = 0
if not test:
    start = 1024

for i in range(start, len(lines)):

    if test:
        arr = plotBytes(i, 7)
    else:
        arr = plotBytes(i, 71)

    res = findBestPath(arr)
    #print(i)
    if res == None:
        print("part 2:", ','.join([str(l) for l in lines[i-1]]))
        break
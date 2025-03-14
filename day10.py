import re
import numpy as np
import itertools
from collections import deque

test = False
day = "10"

if test:
    filename = f"day{day}-input-test.txt"
else:
    filename = f"day{day}-input.txt"


# input parsing
arr = []
with open(filename, "r") as file:

    for line in file:
        row = [int(l) for l in line.strip()]
        arr.append(row)


def OOB(y, x): # check out of bounds
    return y < 0 or y >= len(arr) or x < 0 or x >= len(arr)


def parseTrailheads():
    trailheads = {}

    for y in range(len(arr)):
        #print("".join([str(l) for l in arr[y]]))
        for x in range(len(arr[y])):
            if arr[y][x] == 0:
                trailheads.update({(y,x): []})
    return trailheads


dirs = [(-1,0), (0,1), (1,0), (0,-1)]

def findPaths(part2=False):
    
    trailheads = parseTrailheads()
    
    #for coord, peaks in trailheads.items():
    #    print(coord, peaks)

    for coord in trailheads.keys():
        toVisit = deque()
        alt = 0
        for dir in dirs:
            newY, newX = coord[0] + dir[0], coord[1] + dir[1]
            if not OOB(newY, newX) and arr[newY][newX] == alt+1:
                toVisit.appendleft((newY, newX, arr[newY][newX]))

        while toVisit:
            y, x, alt = toVisit.pop()
            #print(y,x,alt)
            if alt == 9:
                if not part2 and (y,x) in trailheads[coord]:
                    continue
                trailheads[coord].append((y,x))
            for dir in dirs:
                newY, newX = y + dir[0], x + dir[1]
                if not OOB(newY, newX) and arr[newY][newX] == alt+1:
                    toVisit.appendleft((newY, newX, arr[newY][newX]))

    #for coord, peaks in trailheads.items():
    #    print(coord, peaks, len(peaks))
    
    return trailheads


trailheads = findPaths()
print("part 1:", sum([len(peaks) for peaks in trailheads.values()]))

trailheads = findPaths(part2=True)
print("part 2:", sum([len(peaks) for peaks in trailheads.values()]))



"""
Next steps:

iterate over coords
implement deque for toVisit coords using BFS
use set to keep track of visited coords (optional, maybe part2)

if peak is reached, add it to trailhead info if not there already
trailheads[coord].append(peakY, peakX)

count total
"""
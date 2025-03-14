import re
import numpy as np
import itertools
import math
import time
from collections import deque, Counter

test = False
day = "14"

if test:
    filename = f"day{day}-input-test.txt"
else:
    filename = f"day{day}-input.txt"

# input parsing
robots = []
with open(filename, "r") as file:
    for line in file:
        position = [int(x) for x in line.strip().split(' ')[0].split('=')[1].split(',')]
        velocity = [int(x) for x in line.strip().split(' ')[1].split('=')[1].split(',')]
        robots.append((position, velocity))

def printMap(arr):
    with open("day14-output.txt", 'a') as file:
        for row in arr:
            file.write("".join([str(n) for n in row]))
            file.write("\n")
        file.write("\n")

if not test:
    wide = 101
    tall = 103
else:
    wide = 11
    tall = 7

def makeNewArr():
    arr = []
    if not test:
        arr = [[0] * 101 for _ in range(103)]  
    else:
        arr = [[0] * 11 for _ in range(7)]
    return arr

"""arr = makeNewArr()
seconds = 100
for robot in robots:
    x, y = robot[0]
    dx, dy = robot[1]
    finalX = (x + (seconds * dx)) % wide
    finalY = (y + (seconds * dy)) % tall
    #print(x, y, dx, dy)
    print(finalX, finalY)
    arr[finalY][finalX] += 1"""


def countArr(arr):
    return sum([sum(row) for row in arr])

def countRobots(arr):
    quadrants = []
    quadrants.append([row[:int(wide/2)] for row in arr[:int(tall/2)]])
    quadrants.append([row[int(wide/2)+1:] for row in arr[:int(tall/2)]])
    quadrants.append([row[:int(wide/2)] for row in arr[int(tall/2)+1:]])
    quadrants.append([row[int(wide/2)+1:] for row in arr[int(tall/2)+1:]])
    
    qCounts = [countArr(q) for q in quadrants]

    if qCounts[0] == qCounts[1] and qCounts[2] == qCounts[3]:
        printMap(arr)
        time.sleep(2)
        return True

    return False
    #return sum([sum([sum(row) for row in quadrant])] for quadrant in quadrants)
    #return sum()

    pass


#print("part 1:", countRobots(arr))


def checkSymmetry(arr):
    for row in arr:
        for i in range(int(wide / 2)):
            #print(i, wide-i)
            if row[i] != row[wide-i-1]:
                return False
    
    return True




"""
robotXs = [robot[0][0] for robot in robots]
robotYs = [robot[0][1] for robot in robots]
robotdXs = [robot[1][0] for robot in robots]
robotdYs = [robot[1][1] for robot in robots]

i = 1
while True:
    if i % 100000 == 0:
        print(i)
    for n in range(len(robotXs)):
        robotXs[n] = (robotXs[n] + robotdXs[n]) % wide
        robotYs[n] = (robotYs[n] + robotdYs[n]) % tall
    
    maps = set()
    arr = makeNewArr()
    for x, y in zip(robotXs, robotdYs):
        arr[y][x] += 1

    printMap(arr)
    i += 1

"""

i = 1
while(i < 1000000000):
    #arr = makeNewArr()
    robotCoords = set()
    newcoords = []
    #print(i)


    for robot in robots:
        x, y = robot[0]
        dx, dy = robot[1]
        finalX = (x + (i * dx)) % wide
        finalY = (y + (i * dy)) % tall
        #print(finalX, finalY)
        robotCoords.add((finalX, finalY))
        newcoords.append((finalX, finalY))
        #print(finalX, finalY)
        #arr[finalY][finalX] += 1
    
    if i % 101 == 74:
        print(i)
        arr = makeNewArr()
        for r in newcoords:
            #print(r)
            arr[r[1]][r[0]] += 1
        printMap(arr)
        if i == 8154:
            break
    
    i += 1

#print(len(arr), len(arr[0]))
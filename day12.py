import re
import numpy as np
import itertools
from collections import deque, Counter

test = False
day = "12"

if test:
    filename = f"day{day}-input-test.txt"
else:
    filename = f"day{day}-input.txt"


# input parsing
arr = [] # static, only used to check adjacencies
cleared = [] # variable, visited nodes are deleted from this
with open(filename, "r") as file:

    for line in file:
        row = [l for l in line.strip()]
        rowCopy = [l for l in line.strip()]
        arr.append(row)
        cleared.append(rowCopy)

#for row in arr:
#    print("".join(row))

#print(len(arr), len(arr[0]))

def OOB(y, x): # check out of bounds
    return y < 0 or y >= len(arr) or x < 0 or x >= len(arr)


dirs = [(-1,0), (0,1), (1,0), (0,-1)]

def findFirstNode(arr): # traverses 2D array and returns coord of first non-visited node
    y = 0
    for row in arr:
        x = 0
        for r in row:
            if r != ".":
                return (y, x)
            x += 1
        y += 1
    return None


"""
Part 2 Plan:

collect a list of nodes of a given plant (e.g. something like this)

XXXXXX
XX   X
  XXXX

for each row:
    get starts and ends [0-1] -> sides += 2
    move down
    if starts and ends changes, number of sides increase [1-2] -> sides += 2
    sides = [3-6] -> sides += 2
    sides = [3-3] -> sides += 1
    sides = [2-3] -> sides += 1

for each column
sides = [0-0] -> sides += 2
sides = [0-2, 5-5] -> sides += 3
sides = [1-5] -> sides += 1
sides = [2-2] -> sides += 2
sides = [2-2] -> sides += 0
sides = [2-2] -> sides += 0

in this algo, the start must match the start  
 
"""

def countSides(nodeList):
    sides = 0
    nodeList.sort()
    #print(nodeList)

    currRow = nodeList[0][0]
    left = right = nodeList[0][1]
    edges = []
    prevEdges = []
    for node in nodeList:
        y, x = node

        if y == currRow: # same row
            #print(y, x)
            if x == right:
                continue
            elif x == right + 1:
                right = x
            else: # there is a gap
                edges.append((left, right))
                left = right = x # start a new block
        
        else: # diff row
            # account changes in sides
            edges.append((left, right))
            
            #print("edges:", edges)
            #print("prevEdges:", prevEdges)
            #print(y, x)
            for edge in edges:
                left, right = edge
                if (not prevEdges) or left not in [prevEdge[0] for prevEdge in prevEdges]:
                    sides += 1
                if (not prevEdges) or right not in [prevEdge[1] for prevEdge in prevEdges]:
                    sides += 1

            # start new edges

            prevEdges = edges
            currRow = y
            left = x
            right = x
            edges = []
        
    # process last edge
    edges.append((left, right))
    #print("edges:", edges)
    #print("prevEdges:", prevEdges)
    for edge in edges:
        left, right = edge
        if (not prevEdges) or left not in [prevEdge[0] for prevEdge in prevEdges]:
            sides += 1
        if (not prevEdges) or right not in [prevEdge[1] for prevEdge in prevEdges]:
            sides += 1
    
    #print("sides:", sides)
    return sides

def getPrice(cleared, arr):
    totalPrice = 0
    partTwoPrice = 0
    toVisit = deque()
    firstNode = findFirstNode(cleared)

    while firstNode != None:
        toVisit.append(firstNode)

        area = 0
        peri = 0
        visited = []
        while toVisit:
            y, x = toVisit.popleft()
            plant = cleared[y][x]
            if plant == '.': # sometimes the plant gets added to the stack twice before getting cleared
                continue
            #print(y, x, plant)
            area += 1

            for dir in dirs:
                newY, newX = y + dir[0], x + dir[1]
                if OOB(newY, newX):
                    peri += 1
                elif arr[newY][newX] != plant: # out of bounds
                    peri += 1
                    #print("current plant:", plant, " other plant:", arr[newY][newX])
                elif cleared[newY][newX] == '.': # visited already
                    continue
                else: # will visit next
                    toVisit.append((newY, newX))

            cleared[y][x] = '.'
            visited.append((y,x))
            
        
        #for row in cleared:
        #    print("".join(row))

        transposed = [(node[1], node[0]) for node in visited]
        sides = countSides(visited)
        
        sides += countSides(transposed)
    
        print(f'region {plant} has sides of {sides}, area of {area}, and price of {sides * area}')
        partTwoPrice += (area * sides)
        
        print(f'region {plant} has peri of {peri}, area of {area}, and price of {peri * area}')# totalPrice += (area * peri) # for part 1
        totalPrice += (area * peri)

        firstNode = findFirstNode(cleared)


    return totalPrice, partTwoPrice

partOne, partTwo = getPrice(cleared, arr)

print("part 1:", partOne)
print("part 2:", partTwo)


"""
Plan:

BFS with toVisit queue and visited set
    a. check if OOB and whether adjacent plots are same plant or not
    b. increment area count
    c. if adjacent plots aren't same plant, increment perimeter accordingly
    d. if adjacent plot of same plant have not been visited, add to toVisit queue

"""





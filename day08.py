import re
import numpy as np
import itertools

test = False
day = "08"

if test:
    filename = f"day{day}-input-test.txt"
else:
    filename = f"day{day}-input.txt"

# NOTE: this doesn't account for if there are antinodes a third of the way between antennae
# the input just happens to not have xDif and yDif that are both multiples of 3

# input parsing
arr = []
nodes = {}
with open(filename, "r") as file:

    y = 0
    for line in file:
        row = [l for l in line.strip()]

        x = 0
        for pt in row:
            if pt != '.':
                if pt in nodes.keys():
                    nodes[pt].append((y,x))
                else:
                    nodes.update({pt: [(y,x)]})
            x += 1

        arr.append(row)
        y+= 1

# checked that input was square
nodeMap = np.zeros((len(arr), len(arr)))

def inBounds(y,x):
    if y < 0 or y >= len(arr) or x < 0 or x >= len(arr):
        return False
    return True

for node, coords in nodes.items():
    #print(node, coords)

    pairs = itertools.combinations(coords, 2)
    for pair in pairs:
        yDif, xDif = pair[1][0] - pair[0][0], pair[1][1] - pair[0][1]
        #print(pair, yDif, xDif)

        # check before first node
        yNew, xNew = pair[0][0] - yDif, pair[0][1] - xDif
        if inBounds(yNew, xNew):
            nodeMap[yNew][xNew] = 1

        # check after second node
        yNew, xNew = pair[1][0] + yDif, pair[1][1] + xDif
        if inBounds(yNew, xNew):
            nodeMap[yNew][xNew] = 1

#print(nodes)

#for nodeRow in nodeMap:
#    print("".join(str(nodeRow)))

print("part 1:", np.count_nonzero(nodeMap == 1))


for node, coords in nodes.items():
    for coord in coords: # all antennae are nodes
        nodeMap[coord[0]][coord[1]] = 1

    pairs = itertools.combinations(coords, 2)
    for pair in pairs:
        yDif, xDif = pair[1][0] - pair[0][0], pair[1][1] - pair[0][1]

        # check from first node
        yNew, xNew = pair[0][0] - yDif, pair[0][1] - xDif
        while inBounds(yNew, xNew):
            nodeMap[yNew][xNew] = 1
            yNew -= yDif
            xNew -= xDif

        # check from second node
        yNew, xNew = pair[1][0] + yDif, pair[1][1] + xDif
        while inBounds(yNew, xNew):
            nodeMap[yNew][xNew] = 1
            yNew += yDif
            xNew += xDif

print("part 2:", np.count_nonzero(nodeMap == 1))

#for nodeRow in nodeMap:
#    print("".join(str(nodeRow).split('.')))
import re
import numpy as np
import itertools

test = False
day = "09"

if test:
    filename = f"day{day}-input-test.txt"
else:
    filename = f"day{day}-input.txt"

# input parsing
diskMap = []
diskMapCopy = []
with open(filename, "r") as file:

    for line in file:
        line = line + '0'
        #print(len(line))
        for i in range(0, len(line.strip()), 2):
            data = int(line[i])
            gap = int(line[i+1])
            diskMap.append((data, gap))
            diskMapCopy.append((data, gap, False))

for dm in diskMap:
    #print(dm, sum(dm))
    if dm[0] == 0:
        print("zero data")
        break

totalSpace = sum([sum(dm) for dm in diskMap])
totalData = sum([dm[0] for dm in diskMap])


#print(totalData, totalSpace)

    
totalValue = 0
position = 0
i = 0
while i < len(diskMap):
    data, gap = diskMap[i]
    #print(i, data, gap)
    for _ in range(data):
        totalValue += i * position
        #print(i, position, totalValue)
        position += 1
    if i == len(diskMap) -1:
        break
    for _ in range(gap):
        totalValue += ((len(diskMap)-1) * position)
        #print(len(diskMap)-1, position, totalValue)
        if diskMap[-1][0] == 1:
            del diskMap[-1]
        else:
            diskMap[-1] = (diskMap[-1][0]-1, diskMap[-1][1])
        position += 1
    i += 1

print("part 1:", totalValue)


totalValue = 0
position = 0
i = 0
for i in range(len(diskMapCopy)):
    data, gap, moved = diskMapCopy[i]
    #print(i, data, gap, moved)

    # add value of existing data
    if moved:
        position += data # don't add anything if it's been moved
    else:
        for _ in range(data):
            totalValue += i * position
            #print(i, position, totalValue)
            position += 1

    # try and fill gap:
    for j in range(len(diskMapCopy)-1, i, -1):
        if gap >= diskMapCopy[j][0] and diskMapCopy[j][2] == False: # has space and data is unmoved
            for _ in range(diskMapCopy[j][0]): # move data here
                totalValue += j * position
                #print(j, position, totalValue)
                position += 1
            diskMapCopy[j] = (diskMapCopy[j][0], diskMapCopy[j][1], True) # record that data was moved
            
            gap -= diskMapCopy[j][0] # decrement gap size
            if gap == 0:
                break
    
    for _ in range(gap):
        #print(0, position, totalValue)
        position += 1 # increment position without adding to totalValue
    i += 1

print("part 2:", totalValue)




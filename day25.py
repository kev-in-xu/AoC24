import numpy as np
import itertools
import math, time, copy, re
import heapq
from collections import deque, Counter

test = False
day = "25"

if test:
    filename = f"day{day}-input-test.txt"
else:
    filename = f"day{day}-input.txt"

# input parsing
lines = []
with open(filename, "r") as file:
    lines = "".join([line for line in file])

#print(lines)

diagrams = lines.split('\n\n')

def printMap(arr):
    for row in arr:
        print("".join([str(n) for n in row]))

def diagramToArray(diagram):
    arr = []
    for line in diagram.split('\n'):
        line = [c for c in line.strip()]
        arr.append(line)
    return arr

def getHeights(arr): # return heights and whether it is lock or key
    lock = False
    
    #print(arr[0])
    if all([c == '#' for c in arr[0]]):
        lock = True
    printMap(arr)
    
    counts = []
    for a in zip(*arr):
        counts.append(a.count('#')-1)
    #if arr[0] or arr[len(arr)]
    return counts, lock

locks = []
keys = []
for diagram in diagrams:
    arr = diagramToArray(diagram)
    counts, lock = getHeights(arr)
    if lock:
        locks.append(counts)
    else:
        keys.append(counts)


print(locks)
print(keys)

pairs = itertools.product(keys, locks)
print()

def pairPossible(pair):
    for a, b in zip(*pair):
        if a + b > 5:
            return False
    return True

total = 0
for pair in pairs:
    
    if pairPossible(pair):
        total += 1
        print(pair)

print(total)

    
import re
import numpy as np
import itertools
import math
import copy
import heapq
import time
from collections import deque, Counter

test = False
day = "19"

if test:
    filename = f"day{day}-input-test.txt"
else:
    filename = f"day{day}-input.txt"

# input parsing
with open(filename, "r") as file:
    lines = "".join([l for l in file])

    towels, patterns = lines.split('\n\n')
    towels = towels.strip().split(', ')
    patterns = [p.strip() for p in patterns.split('\n')]

#print(towels)
#print(patterns)

def recursiveTryTowels(towels, pattern):
    #print(pattern)
    if not pattern:
        return True
    
    for towel in towels:

        if len(towel) > len(pattern):
            continue

        if towel == pattern[:len(towel)]:
            #print("appending...")
            if recursiveTryTowels(towels, pattern[len(towel):]):
                return True

    return False

ans = []
for pattern in patterns:
    ans.append(recursiveTryTowels(towels, pattern))

print("part 1:", ans.count(True))

"""
For part 2:
Check starting from end, keep track of how many arrangements for that subpattern, and cache the result
When checking longer subpatterns, answer will be newest addition + cached answers

Example:

Towels: 
ABC CDE
AB CD DE
A B C D

Patterns:
ABCDE

E: none (0)
DE: DE (1)
CDE: C (DE), CDE (1*1, 1 -> 2)
BCDE: B (CDE) (1*1 -> 1)
ABCDE: A (BCDE), AB (CDE) (1*1, 1*2 -> 3)
"""

# sorts towels by length and color so that 
towels.sort()
colors = ['b','g','r','u','w']
colorTowels = {}
for color in colors:
    colorTowels[color] = [t for t in towels if t[0] == color]

#print(colorTowels)

patternCache = {} # for saving intermediate results
total = 0
for pattern in patterns:
    for i in range(1,len(pattern)+1):
        subpattern = pattern[-i:]
        #print(subpattern)

        ways = 0
        for towel in colorTowels[subpattern[0]]:
            if len(towel) > len(subpattern): # not sure if it's faster with or without this
                continue

            if towel == subpattern: # same length
                ways += 1
            
            elif towel == subpattern[:len(towel)]: # like B (CDE) example
                ways += patternCache[subpattern[len(towel):]]
        
        patternCache[subpattern] = ways

    total += ways
    #print(ways)

print("part 2:", total)
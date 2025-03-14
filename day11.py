import re
import numpy as np
import itertools
from collections import deque, Counter

test = False
day = "11"

if test:
    filename = f"day{day}-input-test.txt"
else:
    filename = f"day{day}-input.txt"

"""
Tried using stack and represent the line of individual stones, but later switched to a Counter dict
because order doesn't matter and the smaller digits come up much more frequently

Cache was used to store blink results, but probably not necesssary after counter was implemented
"""

# input parsing
nums = []
with open(filename, "r") as file:

    for line in file:
        nums = [int(l) for l in line.strip().split()]

#print(" ".join([str(n) for n in nums]))

def blinkOnce(n): # this method only runs if results not found in cache
    newNums = []
    if n == 0:
        newNums.append(1)
    elif len(str(n)) % 2 == 0:
        newNums.append(int(str(n)[0:int(len(str(n))/2)])) # cast n as str, get first half, then cast back to int
        newNums.append(int(str(n)[int(len(str(n))/2):])) # second half
    else:
        newNums.append(n * 2024)
    
    return newNums

def blink(times):
    depths = [Counter(nums)] # initial input values
    #print(depths[0])

    blinkResult = {0: [1]} # cache of results

    for i in range(times):
        instances = depths[i]
        newInstances = {}

        for k, v in instances.items():

            if k in blinkResult.keys(): # check if result has been cached
                result = blinkResult[k]
            else:
                result = blinkOnce(k)
                blinkResult.update({k: result}) # cache result

            for r in result:
                if r in newInstances.keys():
                    newInstances[r] += v
                else:
                    newInstances[r] = v
        #print("depth:", i)
        depths.append(newInstances)
        #print(newInstances)
    return sum([v for v in depths[times].values()])


print("part 1:", blink(25))
print("part 2:", blink(75))

import numpy as np
import itertools
import math, time, copy, re
import heapq
from collections import deque, Counter

test = False
day = "22"

if test:
    filename = f"day{day}-input-test.txt"
else:
    filename = f"day{day}-input.txt"

# input parsing
inits = []
with open(filename, "r") as file:
    inits = [int(l.strip()) for l in file]

print(inits)

def pruneAndMix(num, factor):
    if factor > 0:
        return ((num << factor) ^ num) % (2 ** 24)
    else:
        return ((num >> -factor) ^ num) % (2 ** 24)

def getNextNum(num):
    num = pruneAndMix(num, 6)
    num = pruneAndMix(num, -5)
    num = pruneAndMix(num, 11)
    return num


total = 0
prices = []
for i in inits:
    final = i
    price = [int(str(i)[-1])]
    for _ in range(2000):
        final = getNextNum(final)
        price.append(int(str(final)[-1]))
        
    #print(f'{i}: {final}')
    total += final
    prices.append(price)

#print(total)
#print(prices)

diffs = []
for price in prices:
    diff = []
    for i in range(len(price)-1):
        print(price[i+1] - price[i])
        diff.append(price[i+1] - price[i])
    diffs.append(diff)

#print(diffs)


# get shortlist of possible signals
sigList = [i for i in range(9,-10,-1)]
#print(sigList)
allSignals = itertools.product(sigList, sigList, sigList, sigList)


def overTen(sig):
    res = sum([s for s in sig])
    #print("res", res)
    return res > 9 or res < -9

def getValidSigs(sigs):
    valids = []
    for sig in sigs:
        #print(sig)
        if overTen(sig):
            continue
        if any([overTen(sig[i:i+3]) for i in range(2)]):
            continue
        if any([overTen(sig[i:i+2]) for i in range(3)]):
            continue
        #print(sig, "is valid")
        valids.append(sig)

    return valids


validSigs = getValidSigs(allSignals)
#print(len(validSigs))

def checkProfits(diffs, prices, validSig, maxProfit):
    profits = 0
    monkeys = []
    for i in range(len(prices)):

        if (len(prices) - i) * 9 < (maxProfit-profits): # if possible remaining points are not enough, return 0
            return 0, []

        diff = diffs[i]
        price = prices[i]

        bought = False
        for j in range(len(price)-3):
            if diff[j] == validSig[0] and diff[j:j+4] == validSig: # first if statement is a shortcut
                #print(f'bought from monkey {i} at time {j} at price {price[j+4]}.')
                monkeys.append((i, j, price[j+4]))
                profits += price[j+4]
                bought = True
                break
        if not bought:
            pass
            #print(f'no purchase from monkey {i}.')

    return profits, monkeys

maxProfit = 0
maxSig = 0
maxMonkeys = []
for sig in validSigs:
    res, monkeys = checkProfits(diffs, prices, list(sig), maxProfit)
    if res > maxProfit:
        print(f'profit from sig {sig} was {res}')
        maxMonkeys = monkeys
        maxProfit = res
        maxSig = sig

print(maxProfit, maxSig, maxMonkeys)


"""
if i were to do this again I can sort by highest anticipated value:

i.e. sort the validSigs by net change after the signal (i.e. 2,3,3,1 before 4,0,1,-1)
    so that there will be more of a speedup with the early loop break based on possible reamining points 

"""


"""
Look into binary sequences and how they change


XXXXXXABCDEF << 6
---
ABCDEF000000 ^ ABCDEF
---
ABCDEFABCDEF
prune
---
ABCDEFABCDEF >> 5
---
XXXXXABCDEFA ^ 
ABCDEFABCDEF
---
XXXXXabcdefa
prune
---
XXXXXabcdefa << 11
---
a00000000000 ^
XXXXXabcdefa
----
xXXXXabcdefa
prune


It's essentailly just ?
ABCDEFA ^
FABCDEF
"""

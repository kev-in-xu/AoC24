import re
import numpy as np
import itertools
import math
import copy
import heapq
import time
from collections import deque, Counter

test = True
day = "21"

if test:
    filename = f"day{day}-input-test.txt"
else:
    filename = f"day{day}-input.txt"

# input parsing
codes = []
with open(filename, "r") as file:
    codes = [l.strip() for l in file]

#print(codes)

"""
Part 1:
num -> numpad coords --> moves on numpad -> wasd keys
-> wasd coords --> moves on keypad -> wasd keys
-> wasd coords --> moves on keypad -> wasd keys -> output
"""

numPad = {'7': (0,3), '8': (1,3), '9': (2,3), 
          '4': (0,2), '5': (1,2), '6': (2,2), 
          '1': (0,1), '2': (1,1), '3': (2,1), 
                      '0': (1,0), 'A': (2,0)}


keyPad = {            '^': (1,1), 'A': (2,1),
          '<': (0,0), 'v': (1,0), '>': (2,0)}

# returns new x y coordinates
def makeMove(x, y, move):
    for m in move:
        if m == '>':
            x += 1
        if m == '<':
            x -= 1
        if m == '^':
            y += 1
        if m == 'v':
            y -= 1
    return x, y

# checks whether a move will end up on an edge. if so, swap ^v moves with <> moves
def checkEdge(move, x, y, num=False):
    if num:
        edge = (0, 0)
    else:
        edge = (0, 1)
    
    x, y = makeMove(x, y, move[0])

    if (x, y) == edge: # if hits edge, swap moves
        temp = move[0]
        x, y = makeMove(x, y, move[1])
        move[0] = move[1]
        move[1] = temp
    return move

"""
IMPORTANT:
I found the below order of <, v, ^, > by trial and error, but below explanation is very clear

In general since each step left is more expensive, 
you always want to hit the far left key first (<), 
and then the middle key (^ or v),
and then a right column key (> or A).

from: https://www.reddit.com/r/adventofcode/comments/1hj7f89/comment/m34erhg/

"""
def getBestMove(coordPair, num=False):
    x, y = coordPair[0]
    diff = (coordPair[1][0] - x, coordPair[1][1] - y)
    #print(coordPair)
    move = []
    if diff[0] < 0:
        move.append('<' * -diff[0])
    if diff[1] < 0:
        move.append('v' * -diff[1])
    if diff[1] > 0:
        move.append('^' * diff[1]) # why should top take precedence over right?
    if diff[0] > 0:
        move.append('>' * diff[0])
    
    move.append('A')
    move = checkEdge(move, x, y, num=num)
    return "".join(move)

# makes cache to figure out best move for each pair of points on the num/key pad
def makeCache(padDict, num=False):
    bestMoves = {}
    pairs = itertools.product(padDict.values(), padDict.values())
    for p in pairs:
        bestMoves[p] = getBestMove(p, num=num)
    return bestMoves
    
numCache = makeCache(numPad, num=True)
keyCache = makeCache(keyPad)
#print(keyCache)

# numToKey
def numToKey(code):
    code = 'A' + code
    res = []
    for i in range(len(code)-1):
        #print(code[i], code[i+1])
        
        res.append(numCache[(numPad[code[i]], numPad[code[i+1]])])
    return "".join(res)

levelCache = {}
def recursiveCount(seq, depth):
    if depth == 0:
        return len(seq) # e.g. ^A returns 2
    
    seq = 'A' + seq # prepend A because every set of moves begins at A

    total = 0
    for i in range(len(seq)-1):
        if (seq[i], seq[i+1], depth) in levelCache.keys(): # if found in cache
            total += levelCache[(seq[i], seq[i+1], depth)]
        else:
            result = recursiveCount(keyCache[(keyPad[seq[i]], keyPad[seq[i+1]])], depth - 1)
            levelCache[(seq[i], seq[i+1], depth)] = result # cache result
            total += result
    
    return total

print("part 1:", sum([recursiveCount(numToKey(code), 2) * int(code[0:3]) for code in codes]))
print("part 2:", sum([recursiveCount(numToKey(code), 25) * int(code[0:3]) for code in codes]))

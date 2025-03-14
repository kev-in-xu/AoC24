import re
import numpy as np
import itertools
import math
import time
import copy
from collections import deque, Counter

test = False
day = "15"

if test:
    filename = f"day{day}-input-test.txt"
else:
    filename = f"day{day}-input.txt"

# input parsing
with open(filename, "r") as file:
    lines = "".join([l for l in file])
    maplines, moves = lines.split('\n\n')
    moves = "".join(moves.split('\n'))

    arr = []
    arrTwo = []
    
    for ml in maplines.split('\n'):
        row = [c for c in ml]
        rowTwo = [c for c in ml.replace('.', '..').replace('@', '@.').replace('O', '[]').replace('#', '##')]
        arrTwo.append(rowTwo)
        arr.append(row)
        
def printMap(arr):
    for row in arr:
        print("".join([n for n in row]))
    print()
    #with open ("day15-output.txt", 'a') as file:
    #    for row in arr:
    #        file.write("".join([n for n in row]) + '\n')
    #    file.write('\n')

def OOB(y, x, arr): # check out of bounds
    return y < 0 or y >= len(arr) or x < 0 or x >= len(arr[0])

def findStart(arr):
    y = 0
    for row in arr:
        x = 0
        for c in row:
            if c == '@':
                return x, y
            x += 1
        y += 1

def checkEmpty(arr, m, x, y):
    
    while True:
        if m == '^':
            y -= 1
        if m == 'v':
            y += 1
        if m == '<':
            x -= 1
        if m == '>':
            x += 1
        if arr[y][x] == '.':
                return True
        if arr[y][x] == '#':
            return False

def move(arr, m, x, y):
    #print("starting move")
    obj = arr[y][x]
    arr[y][x] = '.'
    newX = x
    newY = y
    while True:
        if m == '^':
            newY = y - 1
        if m == 'v':
            newY = y + 1
        if m == '<':
            newX = x - 1
        if m == '>':
            newX = x + 1

        # swap objects
        newObj = arr[newY][newX]    
        arr[newY][newX] = obj

        # '.' means we moved into an empty space already
        # otherwise need to keep pushing objects
        if newObj == '.': 
            return
        
        obj = newObj
        x = newX
        y = newY
        
printMap(arr)
x, y = findStart(arr)

dirs = {'<': (0, -1), '>': (0, 1), '^': (-1, 0), 'v': (1, 0)}

for m in moves:

    # check for empty moveable spot
    # defined as a '.' between current location and the first '#' it sees
    #print("curr loc:", y, x)
    #print(m, dirs[m])
    
    if checkEmpty(arr, m, x, y):
        #print("is empty!")
        move(arr, m, x, y)
        y += dirs[m][0]
        x += dirs[m][1]
    
    #printMap(arr)

def countScore(arr):
    score = 0
    y = 0
    for row in arr:
        x = 0
        for c in row:
            if c == 'O':
                score = score + (100 * y) + x
            x += 1
        y += 1
    return score

print("part 1:", countScore(arr))


def checkEmptyTwo(arrTwo, m, x, y):
    xSet = set()
    newXSet = set()
    xSet.add(x)
    newXSet.add(x)

    if m == '^':
        while True:
            y -= 1
            print("checking y =", y, xSet)
            if all([arrTwo[y][x] == '.' for x in xSet]):
                return True
            newXSet = set([x for x in xSet])
            for x in xSet:
                if arrTwo[y][x] == '[':
                    newXSet.add(x+1)
                if arrTwo[y][x] == ']':
                    newXSet.add(x-1)
                if arrTwo[y][x] == '.':
                    newXSet.remove(x)
                if arrTwo[y][x] == '#':
                    return False
            xSet = newXSet
    
    if m == 'v':
        while True:
            y += 1
            print("checking y =", y, xSet)
            if all([arrTwo[y][x] == '.' for x in xSet]):
                return True
            newXSet = set([x for x in xSet])
            for x in xSet:
                if arrTwo[y][x] == '[':
                    newXSet.add(x+1)
                if arrTwo[y][x] == ']':
                    newXSet.add(x-1)
                if arrTwo[y][x] == '.':
                    newXSet.remove(x)
                if arrTwo[y][x] == '#':
                    return False
            xSet = newXSet
    
    if m == '<':
        while True:
            x -= 1
            if arrTwo[y][x] == '.':
                    return True
            if arrTwo[y][x] == '#':
                return False
    
    if m == '>':
        while True:
            x += 1
            if arrTwo[y][x] == '.':
                    return True
            if arrTwo[y][x] == '#':
                return False

def moveTwo(arrTwo, m, x, y):
    #print("starting move")
    obj = arrTwo[y][x]
    objDict = {x: obj}
    newObjDict = {}
    arrTwo[y][x] = '.' # replace original '@' with '.'
    newX = x
    newY = y

    if m == '^':
        while True:
            newY = y - 1 # increment coord

            newObjDict = {}
            # check newObjDict using existing x's
            for x in objDict.keys():
                newObjDict[x] = arrTwo[newY][x]

            # complete newObjDict by checking []s
            tempDict = {}
            for x, obj in newObjDict.items():
                if x+1 not in newObjDict.keys() and obj == '[':
                    tempDict.update({x+1: ']'})
                if x-1 not in newObjDict.keys() and obj == ']':
                    tempDict.update({x-1: '['})
            
            newObjDict.update(tempDict)

            # iterate over newObjDict keys, filling in with objDict or '.'
            print("filling in row", newY, "with", objDict)

            for x in newObjDict.keys():
                if x in objDict.keys():
                    arrTwo[newY][x] = objDict[x]
                else:
                    arrTwo[newY][x] = '.'

            if all([obj == '.' for _, obj in newObjDict.items()]):
                return
            
            objDict = copy.deepcopy(newObjDict)
            removeList = []

            for x, obj in objDict.items():
                if obj == '.':
                    removeList.append(x)
            
            for x in removeList:
                objDict.pop(x)
            
            x = newX
            y = newY


   
    if m == 'v':
        while True:
            newY = y + 1

            newObjDict = {}
            # check newObjDict using existing x's
            for x in objDict.keys():
                newObjDict[x] = arrTwo[newY][x]

            # complete newObjDict by checking []s
            tempDict = {}
            for x, obj in newObjDict.items():
                if x+1 not in newObjDict.keys() and obj == '[':
                    tempDict.update({x+1: ']'})
                if x-1 not in newObjDict.keys() and obj == ']':
                    tempDict.update({x-1: '['})
            
            newObjDict.update(tempDict)

            # iterate over newObjDict keys, filling in with objDict or '.'
            print("filling in row", newY, "with", objDict)

            for x in newObjDict.keys():
                if x in objDict.keys():
                    arrTwo[newY][x] = objDict[x]
                else:
                    arrTwo[newY][x] = '.'

            if all([obj == '.' for _, obj in newObjDict.items()]):
                return
            
            objDict = copy.deepcopy(newObjDict)
            removeList = []

            for x, obj in objDict.items():
                if obj == '.':
                    removeList.append(x)
            
            for x in removeList:
                objDict.pop(x)
            
            x = newX
            y = newY

    
    if m == '<':
        while True:
            print("working")
            newX = x - 1
            # swap objects
            newObj = arrTwo[newY][newX]    
            arrTwo[newY][newX] = obj

            # '.' means we moved into an empty space already
            # otherwise need to keep pushing objects
            if newObj == '.': 
                return
            
            obj = newObj
            x = newX
            y = newY
    
    if m == '>':
        while True:
            newX = x + 1
            # swap objects
            newObj = arrTwo[newY][newX]    
            arrTwo[newY][newX] = obj

            # '.' means we moved into an empty space already
            # otherwise need to keep pushing objects
            if newObj == '.': 
                return
            
            obj = newObj
            x = newX
            y = newY
        

printMap(arrTwo)
x, y = findStart(arrTwo)

for m in moves:

    # check for empty moveable spot
    # defined as a '.' between current location and the first '#' it sees
    print("curr loc:", y, x)
    print(m, dirs[m])
    
    if checkEmptyTwo(arrTwo, m, x, y):
        moveTwo(arrTwo, m, x, y)
        y += dirs[m][0]
        x += dirs[m][1]
    else:
        print('movement blocked')
    printMap(arrTwo)

def countScoreTwo(arrTwo):
    score = 0
    y = 0
    for row in arrTwo:
        x = 0
        for c in row:
            if c == '[':
                score = score + (100 * y) + x
            x += 1
        y += 1
    return score

print("part 2:", countScoreTwo(arrTwo))
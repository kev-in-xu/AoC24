import re
import numpy as np
import itertools
from collections import deque, Counter

test = False
day = "13"

if test:
    filename = f"day{day}-input-test.txt"
else:
    filename = f"day{day}-input.txt"


# input parsing
claws = []
with open(filename, "r") as file:
    lines = "".join([l for l in file])

    for line in lines.split('\n\n'):
        claw = []
        for rule in line.split('\n'):
            claw.append([int(coord[2:]) for coord in rule.split(': ')[1].split(', ')])
        claws.append(claw)

#for claw in claws:
#    print(claw)


"""
Plan: try and use a greedy algorithm:

Use as many B's as possible, then add A's and subtact B's.

First, calculate how many B's it'd take to get close to the answer

min(prizeX / BX, prizeY / BY)


"""
cost = 0
for claw in claws:
    a, b, prize = claw
    prize = [prize[0] + 10000000000000, prize[1] + 10000000000000]



    bCount = ((prize[1] * a[0]) - (a[1] * prize[0])) / ((b[1] * a[0]) - (a[1] * b[0])) # solve linear equation
    #print(bCount)
    

    if bCount == int(bCount):
        #aCount = (bCount * b[0] - prize[0]) / a[0]
        #print(bCount * b[0] - prize[0])
        aCount = ((prize[0] - (b[0] * bCount)) / a[0])
        if aCount == int(aCount):
            #print(aCount, bCount)
            print(aCount * a[0] + bCount * b[0], prize[0])
            print(aCount * a[1] + bCount * b[1], prize[1])
            cost += (aCount * 3 + bCount)
        

    #print(round(prize[0] / b[0]))

    #bCount = round(prize[0] / b[0]), 100
    #aCount = 0
    
    #if prize[0] > 100 * (a[0] + b[0]) or prize[1] > 100 * (a[1] + b[1]):
    #    print("coord bigger than 100 of both buttons")
    #    continue


    """
    I need to solve ax + by = c and find integer solutions

    

    while bCount > 0:
        x = aCount * a[0] + bCount * b[0]

        if prize[0] > x:
            aCount += 1
            continue
    
        if prize[0] < x:
            bCount -= 1
            continue

        if x == prize[0]:
            y = aCount * a[1] + bCount * b[1]
            if y == prize[1]:
                print(f'aCount: {aCount}, bCount: {bCount}, cost: {aCount * 3 + bCount}')
                cost += (aCount * 3 + bCount)
                break




        
        
        
        if aCount == 100:
            bCount -= 1
            aCount = 0
            continue
        aCount += 1
    """
            
        
        


    #print(a, b, prize, bCount)

print("cost:", cost)
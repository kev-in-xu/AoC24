import numpy as np
import itertools
import math, time, copy, re
import heapq
from collections import deque, Counter

test = False
day = "23"

if test:
    filename = f"day{day}-input-test.txt"
else:
    filename = f"day{day}-input.txt"

# input parsing
connects = [] # connects is a list of 2-comp connections
with open(filename, "r") as file:
    lines = [l.strip() for l in file]
    for line in lines:
        connects.append(tuple(line.split('-')))

# stations is a set of computers
stations = set()
for c in connects:
    stations.add(c[0])
    stations.add(c[1])
    #print(c)

stations = sorted(list(stations)) # sorts stations
#print(stations)

adjList = {} # adjacency list for graph representation
for station in stations:
    adjList[station] = []

for c in connects: # bi-directional connections added
    adjList[c[0]].append(c[1])
    adjList[c[1]].append(c[0])

for k, v in adjList.items():
    adjList[k] = sorted(v)


def getTrios(adjList):
    groups = set() # gets a group of 3
    for s, c in adjList.items():
        #print(s)
        pairs = itertools.combinations(c, 2)
        for p in pairs:
            if p[1] in adjList[p[0]]:
                groups.add(tuple(sorted([s, p[0], p[1]])))
                #print(s, p[0], p[1], "is a group")
    return groups

def partOne(adjList):
    groups = getTrios(adjList)
    total = 0
    for g in sorted(list(groups)):
        #print(','.join(g))
        if any([s[0] == 't' for s in g]):
            total += 1
            #print(",".join(g))
    return total

print("part 1:", partOne(adjList))

def iterativeSolve(adjList, connects, groupSize, ans):

    """if groupSize == 6: # test case
        for adj in adjList.items():
            print(adj)
        return adjList"""
    
    if all([v == [] for v in adjList.values()]):
        #print(groupSize)
        return groupSize - 1, ans

    newAdjList = {}
    for k in adjList.keys(): # initialize new adjList of next depth
        newAdjList[k] = []

    for station, groups in adjList.items(): # station, connected computers
        #print()
        #print(station)

        for group in groups:
            for k, v in adjList.items():
                #print(group, k, v)
                if group in v and station != k:
                    #print(f'{station}-{group}, {k}-{group}, {station}-{k}?')
                    if tuple([k, station]) in connects or tuple([station, k]) in connects:
                        if type(group) is str:
                            g = [group]
                        else:
                            g = list(group)
                        newSortedGroup = tuple(sorted([station] + [k] + g))
                        #print(newSortedGroup)

                        if tuple(newSortedGroup[1:]) not in newAdjList[newSortedGroup[0]]:
                            newAdjList[newSortedGroup[0]].append(tuple(newSortedGroup[1:]))
                            #print(newSortedGroup, "is a group")
                        else:
                            pass
                            #print("group already made")
                    else:
                        pass
                        #print(f'{station} does not connect to {k}')
    
    
    for k, v in adjList.items():
        if v != []:
            ans = f'{k},{",".join(v[0])}'
            #print(f'{k},{",".join(v[0])}')
            break
    
    return iterativeSolve(newAdjList, connects, groupSize + 1, ans)


res = iterativeSolve(adjList, connects, 2, "")
print("part 2:", res[1]) # res[0] is the length
    

import numpy as np
import itertools
import math, time, copy, re
import heapq
from collections import deque, Counter

test = False # final solved by parsing output of ordered gates
day = "24"

if test:
    filename = f"day{day}-input-test.txt"
else:
    filename = f"day{day}-input.txt"

# input parsing
lines = []
with open(filename, "r") as file:
    lines = "".join([line for line in file])

#print(lines)

inits, rules = lines.split('\n\n')

nodes = {}
for init in inits.split('\n'):
    node, value = init.split(': ')
    nodes[node] = value == '1'

# need to come up with ordering of rules

# check inputs, if inputs are in existing nodes, append
# if not, ignore and keep iterating

def orderRules(rules, nodes):

    print(rules)
    addedRules = set()
    addedNodes = set()
    ordered = []

    # add x and y nodes into addedRules
    for node in nodes.keys():
        addedNodes.add(node)

    rules = rules.split('\n')

    depth = 0
    while len(addedRules) != len(rules):
        print()
        print("depth=", depth)
        depth += 1
        for rule in rules:
            elements = rule.split(' ')
            a, op, b, dest = elements[0], elements[1], elements[2], elements[4]
            a, b = sorted([a, b])

            if a in addedNodes and b in addedNodes and rule not in addedRules:
                print(a, op, b, dest)
                addedRules.add(rule)
                ordered.append((a, op, b, dest))
                addedNodes.add(dest)
                nodes[dest] = False
            
    
    return ordered, nodes

            
    
ordered, nodes = orderRules(rules, nodes)

for rule in ordered:
    a, op, b, dest = rule
    if op == 'AND':
        nodes[dest] = nodes[a] & nodes[b]
    elif op == 'OR':
        nodes[dest] = nodes[a] | nodes[b]
    elif op == 'XOR':
        nodes[dest] = nodes[a] ^ nodes[b]

    print(rule)

for k, v in nodes.items():
    if k[0] == 'z':
        pass
        #print(k, v)
    
zs = sorted([node for node in list(nodes) if node[0] == 'z'])

res = 0
pwr = 0
for z in zs:
    if nodes[z]:
        res += 2 ** pwr
    pwr += 1

#print(res)

layerOne = []
for rule in ordered:
    if rule[0][0] == 'y' or rule[0][0] == 'x':
        a, op , b, dest = rule
        a, b = sorted([a, b])
        layerOne.append((a, op, b, dest))
    

for rule in sorted(layerOne):
    a, op, b, dest = rule
    print(a, op, b, dest)
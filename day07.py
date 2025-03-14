import re
import numpy as np
import itertools

test = False
day = "07"

if test:
    filename = f"day{day}-input-test.txt"
else:
    filename = f"day{day}-input.txt"

lines = []
with open(filename, "r") as file:
    for line in file:
        ans, inputs = line.split(':')
        inputs = [int(n) for n in inputs.strip().split()]
        lines.append((int(ans), inputs))


def runCalculations(ruleSet):
    total = 0
    for line in lines:
        ans, inputs = line

        numOps = len(line[1])-1
        opSets = itertools.product(ruleSet, repeat=numOps)
        for opSet in opSets:
            sum = inputs[0]
            for i in range(len(opSet)):
                if opSet[i] == '|': # concat
                    sum = sum * (10 ** len(str(inputs[i+1]))) + inputs[i+1]
                elif opSet[i] == '+':
                    sum += inputs[i+1]
                else:
                    sum *= inputs[i+1]
                if sum > ans: # especially useful for part 2 where concat leads to learge numbers
                    break
            if sum == ans:
                total += ans
                break
    return total

print("part 1:", runCalculations(('+','*')))
print("part 2:", runCalculations(('+','*','|')))




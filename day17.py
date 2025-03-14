import re
import numpy as np
import itertools
import math
import copy
import heapq
import time
from collections import deque, Counter

test = False
day = "17"

if test:
    filename = f"day{day}-input-test.txt"
else:
    filename = f"day{day}-input.txt"

# input parsing
with open(filename, "r") as file:
    lines = "".join([l for l in file])

    regsLine, progLine = lines.split('\n\n')
    regs = [int(a.strip().split(': ')[1]) for a in regsLine.split('\n')]
    prog = [int(n) for n in progLine.strip().split(': ')[1].split(',')]


def readCombo(regs, code):
    if code <= 3:
        return code
    if code <= 6:
        return regs[code-4]
    else:
        return "ERROR"
    


def playRules(regs, opcode, operand, instr):
    
    output = None

    newRegs = copy.copy(regs)
    newInstr = copy.copy(instr)

    match opcode:
        case 0: # adv
            newRegs[0] = int(regs[0] / (2 ** readCombo(regs, operand)))
        case 1: # bxl
            newRegs[1] = regs[1] ^ operand
        case 2: # bst
            newRegs[1] = readCombo(regs, operand) % 8
        case 3: # jnz
            if regs[0] != 0:
                #print("jumping")
                newInstr = operand - 2 # jumps and -2 to cancel out final statement
        case 4: # bxc
            newRegs[1] = regs[1] ^ regs[2]
        case 5: # output
            output = readCombo(regs, operand) % 8
        case 6: # bdv
            newRegs[1] = int(regs[0] / (2 ** readCombo(regs, operand)))
        case 7: # cdv
            newRegs[2] = int(regs[0] / (2 ** readCombo(regs, operand)))
    
    return newRegs, newInstr + 2, output


instr = 0 # instruction pointer
#print(prog)
#print(regs, instr)
res = []
while instr < len(prog):
    opcode, operand = prog[instr:instr+2]

    regs, instr, output = playRules(regs, opcode, operand, instr)
    #print(regs, instr)

    if output is not None:
        res.append(output)

print("part 1:", ",".join([str(n) for n in res]))

"""
The eight instructions are as follows:

The adv instruction (opcode 0) performs division. The numerator is the value in the A register. 
The denominator is found by raising 2 to the power of the instruction's combo operand. 
(So, an operand of 2 would divide A by 4 (2^2); an operand of 5 would divide A by 2^B.) 
The result of the division operation is truncated to an integer and then written to the A register.

The bxl instruction (opcode 1) calculates the bitwise XOR of register B and the instruction's literal operand, 
then stores the result in register B.

The bst instruction (opcode 2) calculates the value of its combo operand modulo 8 (thereby keeping only its lowest 3 bits), then writes that value to the B register.

The jnz instruction (opcode 3) does nothing if the A register is 0. However, if the A register is not zero, it jumps by setting the instruction pointer to the value of its literal operand; if this instruction jumps, the instruction pointer is not increased by 2 after this instruction.

The bxc instruction (opcode 4) calculates the bitwise XOR of register B and register C, then stores the result in register B. (For legacy reasons, this instruction reads an operand but ignores it.)

The out instruction (opcode 5) calculates the value of its combo operand modulo 8, then outputs that value. (If a program outputs multiple values, they are separated by commas.)

The bdv instruction (opcode 6) works exactly like the adv instruction except that the result is stored in the B register. (The numerator is still read from the A register.)

The cdv instruction (opcode 7) works exactly like the adv instruction except that the result is stored in the C register. (The numerator is still read from the A register.)

"""

x = 24

def findBits(curr, digit):
    res = []
    for i in range(8):
        a = curr * 8 + i
        b = a % 8
        b = b ^ 5
        c = int(a / (2**b))
        b = b ^ c
        b = b ^ 6
        if b % 8 == digit:
            res.append(i)
    return res


digits = [2,4,1,5,7,5,4,5,0,3,1,6,5,5,3,0]

original = 0
#print('part 2')
for digit in digits[::-1]:
    #print(digit)
    possNextDigits = findBits(original, digit)
    for nd in possNextDigits:
        original = original * 8 + nd
    

def recursiveFind(digits, initials):
    #print(digits, initials)

    for initial in initials:
        if not digits:
            return [initial]
        
        dtr = digits[-1] # digit to reconstruct
        possNextDigits = findBits(initial, dtr)

        if possNextDigits:
            res = []
            for pnd in possNextDigits:
                res.append(recursiveFind(digits[:-1], [(initial * 8) + pnd]))
            return list([r for r in res if r is not None])
        else:
            #print("not the bottom")
            return None
            
#print(recursiveFind(digits, [0]))
nestedAnswers = recursiveFind(digits, [0])

answers = []

def openAndCheck(possList):
    if type(possList) is list:
        for i in possList:
            openAndCheck(i)
    else:
        answers.append(possList)

openAndCheck(nestedAnswers)
# print('nested answers', answers)
print("part 2:", min(answers))
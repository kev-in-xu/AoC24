import re
test = False
day = "05"

if test:
    start = 21
    filename = f"day{day}-input-test.txt"
else:
    start = 1176
    filename = f"day{day}-input.txt"


arr = []
# copy over input from https://adventofcode.com/2024/day/{day}/input into "day{day}-input.txt"
with open(filename, "r") as file:
    lines = [line.strip() for line in file]

rules = []

for line in lines[:start]:
    before, after = line.split('|')
    rules.append((int(before), int(after)))

seqs = []
for line in lines[start+1:]:
    seqs.append([int(i) for i in line.split(',')])

print(seqs[0])
sum = 0
seq = seqs[0]
bads = []
for seq in seqs:
    ok = True
    for rule in rules:
        if rule[0] in seq:
            try:
                if seq.index(rule[1]) < seq.index(rule[0]):
                    ok = False
                    break
            except:
                continue
    if not ok:
        print(seq, "is bad")
        bads.append(seq)
    else:
        print(seq, "is good")
        sum += seq[int((len(seq)-1)/2)]

print(sum)

def recursive_checkrule(seq, rules):
    for rule in rules:
        if rule[0] in seq:
            try:
                if seq.index(rule[0]) > seq.index(rule[1]):
                    print(seq, "doesn't work because of rule", rule)
                    print("moving", rule[1], "over")
                    seq.remove(rule[1])
                    seq.insert(seq.index(rule[0])+1,rule[1])
                    print("new seq:", seq)
                    print()
                    return recursive_checkrule(seq, rules)
            except:
                continue
    print("passed all tests!")
    print()
    return seq[int((len(seq)-1)/2)]


sum = 0
for bad in bads:
    sum += recursive_checkrule(bad, rules)
print(sum)
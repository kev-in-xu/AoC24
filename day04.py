part2 = False
import re

arr = []
# copy over input from https://adventofcode.com/2024/day/3/input into "day03-input.txt"
with open("day04-input.txt", "r") as file:
    for line in file:
        row = [l for l in line.strip()]
        arr.append(row)

def findXMAS(arr):
    return sum([len(re.findall('XMAS', "".join(row))) + len(re.findall('SAMX', "".join(row))) for row in arr])
    # above code is equivalent to:
    """
    total = 0
    for row in arr:
        forward = re.findall('XMAS', "".join(row))
        backward = re.findall('SAMX', "".join(row))
        total += len(forward)
        total += len(backward)
    return total
    """
# arr = list of rows

# construct a list of columns
columns = []
for i in range(len(arr[0])):
    column = [row[i] for row in arr]
    columns.append(column)

# construct list of diagonals (in both '/' and '\' directions)
back_diags = [] # '/'
fwd_diags = [] # '\'
for i in range(len(arr) + len(arr[0])):
    fwd_diag = []
    back_diag = []
    for j in range(i+1):
        if j < len(arr) and i-j < len(arr[0]):
            back_diag.append(arr[j][i-j])
        if len(arr)-1-j >= 0 and i-j < len(arr[0]):
            fwd_diag.append(arr[len(arr)-1-j][i-j])
    back_diags.append(back_diag)
    fwd_diags.append(fwd_diag)

print("part 1: ", findXMAS(arr) + findXMAS(columns) + findXMAS(back_diags) + findXMAS(fwd_diags))

total = 0
for i in range(len(arr)-2): # subtract 2 because we will check a 3x3 grid
    for j in range(len(arr[0])-2):
        box = arr[i][j:j+3] + arr[i+1][j:j+3] + arr[i+2][j:j+3]
        box_str = "".join(box) # joins 3x3 grid as length 9 string

        # possible X_MAS arrangements in regex form
        X_MAS_arrangements = ["S.S.A.M.M", "S.M.A.S.M", "M.S.A.M.S", "M.M.A.S.S"]

        if any(len(re.findall(X_MAS, box_str)) == 1 for X_MAS in X_MAS_arrangements):
            total += 1

print("part 2: ", total)
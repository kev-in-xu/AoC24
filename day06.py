import re
import numpy as np

test = False
day = "06"

if test:
    filename = f"day{day}-input-test.txt"
else:
    filename = f"day{day}-input.txt"

arr = []
with open(filename, "r") as file:
    for line in file:
        row = [l for l in line.strip()]
        if '^' in row:
            x = row.index('^')
            y = len(arr)
        arr.append(row)



width = len(arr[0])
length = len(arr)

primes = [2,3,5,7]

#for row in arr:
#    print("".join(row))
#print(y, x) # starting location

def checkLoop():
    dirs = [(-1,0), (0,1), (1,0), (0,-1)]
    dir = 0
    visited = np.ones((length, width))
    coord = (y,x)

    while True:
        
        new_coord = (coord[0] + dirs[dir][0], coord[1] + dirs[dir][1])
        if new_coord[0] < 0 or new_coord[0] >= width or new_coord[1] < 0 or new_coord[1] >= length:
            return 0
        elif arr[new_coord[0]][new_coord[1]] == '#':
            dir = (dir + 1) % 4
            continue
        else:
            if visited[new_coord[0]][new_coord[1]] % primes[dir] == 0: # loop detection
                return 1
            visited[new_coord[0]][new_coord[1]] *= primes[dir]
            arr[new_coord[0]][new_coord[1]] = 'X'
            coord = new_coord

checkLoop()

#for row in arr:
#    print("".join(row))

ans = sum([row.count('X') for row in arr]) + sum([row.count('^') for row in arr]) 
print("part 1 answer:", ans)
print("part 2 takes a sec...")

valid_obstacles = 0
count = 0
i = 0
for row in arr:
    j = 0
    for char in row:
        if char == 'X':
            arr[i][j] = '#'
            if checkLoop():
                valid_obstacles += 1
                #for r in arr:
                #    print("".join(r))
            arr[i][j] = '.'
        j += 1
        count += 1
        #print(count)
    i += 1

print("part 2 answer:", valid_obstacles)


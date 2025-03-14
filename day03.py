part2 = True

# copy over input from https://adventofcode.com/2024/day/3/input into "day03-input.txt"
with open("day03-input.txt", "r") as file:
    lines = [line.strip() for line in file]


sum = 0

def checkline(line):
    temp_sum = 0
    left_sides = line.split("mul(")
    for left in left_sides:
        right = left.split(")")[0]
        #print(right)
        if right.count(',') == 1:
            first, second = right.split(',')
            #print(first, second)
            if first.isnumeric() and second.isnumeric():
                #print("yes")
                temp_sum += int(first) * int(second)
    return temp_sum


"""for line in lines:
    left_sides = line.split("mul(")
    for left in left_sides:
        right = left.split(")")[0]
        print(right)
        if right.count(',') == 1:
            first, second = right.split(',')
            print(first, second)
            if first.isnumeric() and second.isnumeric():
                print("yes")
                sum += int(first) * int(second)
"""
bigline = ''.join(lines)
dos = bigline.split("do()")
only_dos = [do.split("don't()")[0] for do in dos]
for only_do in only_dos:
    print(only_do)
    sum += checkline(only_do)

print("sum =", sum)
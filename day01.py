part2 = False

left = []
right = []

with open("day01-input.txt", "r") as file:
    for line in file:
        row = line.split()
        left.append(int(row[0]))
        right.append(int(row[1]))

left.sort()
right.sort()

sum = 0

# part 1
if not part2:
    for i in range(1000):
        sum += abs(left[i] - right[i])

#part 2
else:
    for l in left:
        sum += right.count(l) * l

print(sum)
part2 = True

# copy over input from https://adventofcode.com/2024/day/2/input into "day02-input.txt"
with open("day02-input.txt", "r") as file:
    lines = [line.strip() for line in file]

def checkline(nums):
        # creates a list of difference between subsequent list elements
        diff_list = [nums[i+1] - nums[i] for i in range(len(nums)-1)]

        # checks strictly increasing by 1/2/3 or stricting decreasing by 1/2/3
        return set(diff_list).issubset((1,2,3)) or set(diff_list).issubset((-1,-2,-3))

sum = 0

for line in lines:
    nums = [int(num) for num in line.split()] # split line into list of ints
    if checkline(nums):
        sum += 1
    elif part2: # brute force check of lists without one element
        for i in range(len(nums)):
            a = nums.copy()
            del a[i]
            if checkline(a):
                sum += 1
                break

print(sum)
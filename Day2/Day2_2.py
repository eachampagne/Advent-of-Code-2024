#Advent of Code 2024 Day 2 Part 2
#Solved Dec. 2, 2024

#pull check out into function so I can run various combinations of levels
def is_safe(report):
    report_not_decreasing = ((report[1]-report[0]) == abs(report[1] - report[0])) #a boolean - gives true if the difference between the first two terms matches the sign of the difference (i.e., the difference is positive or zero), returns false if difference is decreasing
    #the zero case will be dealt with by the test for the difference being within acceptable bounds
    #it doesn't matter if the first pair is the only odd one out (e.g., the first pair is increasing and all others are decreasing, but this test labels the whole report as increasing despite being the minority)
    #any discrepancy at all fails the safety check

    safe = True

    #iterate through each adjacent pair
    for i in range(len(report)-1):
        first_level = report[i]
        second_level = report[i+1]

        difference = second_level - first_level
        difference_not_decreasing = (difference == abs(difference))
        if difference_not_decreasing != report_not_decreasing:
            safe = False #not safe because not all levels moving in the same direction
            break
        if abs(difference) < 1 or abs(difference) > 3:
            safe = False #difference either too high or zero, either of which is unsafe
            break

    return safe

#f = open("sample.txt")
f = open("input.txt")

no_safe = 0

#Iterate through the input
for i in f:
    levels_str = i.split()
    levels = []
    for j in levels_str:
        levels.append(int(j))

    safe = is_safe(levels)

    #if it doesn't work, try every possible set of removing one level
    #this is definitely not efficient, considering how many times I have to copy the list
    #but it's less likely to introduce logic bugs than coding the logic myself, and inevitably missing edge cases or something
    if not safe:
        for j in range(len(levels)):
            new_levels = levels.copy()
            new_levels.pop(j)
            safe = is_safe(new_levels)
            if safe:
                break

    if safe:
        no_safe += 1

print(no_safe)

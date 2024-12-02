#Advent of Code 2024 Day 2 Part 1
#Solved Dec. 2, 2024

#f = open("sample.txt")
f = open("input.txt")

no_safe = 0

#Iterate through the input
for i in f:
    levels_str = i.split()
    levels = []
    for j in levels_str:
        levels.append(int(j))

    report_not_decreasing = ((levels[1]-levels[0]) == abs(levels[1] - levels[0])) #a boolean - gives true if the difference between the first two terms matches the sign of the difference (i.e., the difference is positive or zero), returns false if difference is decreasing
    #the zero case will be dealt with by the test for the difference being within acceptable bounds
    #it doesn't matter if the first pair is the only odd one out (e.g., the first pair is increasing and all others are decreasing, but this test labels the whole report as increasing despite being the minority)
    #any discrepancy at all fails the safety check
    safe = True

    #iterate through each adjacent pair
    for j in range(len(levels)-1):
        first_level = levels[j]
        second_level = levels[j+1]

        difference = second_level - first_level
        difference_not_decreasing = (difference == abs(difference))
        if difference_not_decreasing != report_not_decreasing:
            safe = False #not safe because not all levels moving in the same direction
            break
        if abs(difference) < 1 or abs(difference) > 3:
            safe = False #difference either too high or zero, either of which is unsafe
            break

    if safe:
        no_safe += 1

print(no_safe)

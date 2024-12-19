#Advent of Code 2024 Day 19 Part 2
#Solved Dec. 19, 2024

#Well I thought this would be easy but it's taking longer to run than I expected
#Guess this calls for memoization

#f = open("sample.txt")
f = open("input.txt")

#returns number of possible designs
def find_combinations(design):
    if design in computed_combos.keys():
        return computed_combos[design]
    combos = 0
    for i in patterns:
        if i == design:
            combos += 1
        elif i == design[:len(i)]:
            combos += find_combinations(design[len(i):])
    computed_combos[design] = combos
    return combos

lines = f.read().strip().split("\n") #need the strip to not get an empty string at the end because of the final \n

#"global" variable referenced in function - this feels sloppy, but is faster than copying
patterns = list(map(str.strip, lines[0].split(",")))

#another "global" variable of form design: combinations to avoid recalculating
computed_combos = {}

design_combos = 0
for i in range(2, len(lines)):
    design = lines[i]

    design_combos += find_combinations(design)

print(design_combos)

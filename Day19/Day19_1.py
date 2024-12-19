#Advent of Code 2024 Day 19 Part 1
#Solved Dec. 19, 2024

#f = open("sample.txt")
f = open("input.txt")

#returns True if possible, False if impossible
def can_create_design(design):
    for i in patterns:
        if i == design:
            return True
        if i == design[:len(i)]:
            if can_create_design(design[len(i):]):
                return True
    return False

lines = f.read().strip().split("\n") #need the strip to not get an empty string at the end because of the final \n

#"global" variable referenced in function - this feels sloppy, but is faster than copying
patterns = list(map(str.strip, lines[0].split(",")))

possible_designs = 0
for i in range(2, len(lines)):
    design = lines[i]

    if can_create_design(design):
        possible_designs += 1

print(possible_designs)

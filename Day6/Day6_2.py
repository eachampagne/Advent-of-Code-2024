#Advent of Code 2024 Day 6 Part 2
#Solved Dec. 6, 2024

#f = open("sample.txt")
f = open("input.txt")

#  -----> x
# |
# |
# |
# |
# |
# v y

obstacles = {}
visited = set()
#Facings:
#   > 0
#   v 1
#   < 2
#   ^ 3
#As in 2022 Day 22 

y = 0
for i in f:
    y += 1 #grid coordinates start at (1, 1)
    x = 0
    for j in i.strip():
        x += 1
        if j == "#":
            obstacles[(x, y)] = True
        elif j == "^": #only necessary ones
            start_pos = (x, y)
            visited.add(start_pos)
            start_facing = 3
        elif j == ">": #this and next 2 are for generality - it would bother me if I didn't have these
            start_pos = (x, y)
            visited.add(start_pos)
            start_facing = 0
        elif j == "v":
            start_pos = (x, y)
            visited.add(start_pos)
            start_facing = 1
        elif j == "<":
            start_pos = (x, y)
            visited.add(start_pos)
            start_facing = 2

height = y
width = x

not_finished = True

current_pos = start_pos
facing = start_facing

#go through original path to find possible places to put obstacles
#there's no point trying an obstacle somewhere the guard will never run into
#this also cuts the number of places to check from (grid size - obstacles - starting position)
#to (Part 1 answer - starting position), which is about half the length
while not_finished:
    match facing:
        case 0:
            target_pos = (current_pos[0] + 1, current_pos[1])
        case 1:
            target_pos = (current_pos[0], current_pos[1] + 1)
        case 2:
            target_pos = (current_pos[0] - 1, current_pos[1])
        case 3:
            target_pos = (current_pos[0], current_pos[1] - 1)
    if target_pos[0] <= 0 or target_pos[0] > width or target_pos[1] <= 0 or target_pos[1] > height:
        not_finished = False
        break
    elif obstacles.get(target_pos, False):
        facing = (facing + 1) % 4
        continue
    else:
        current_pos = target_pos
        visited.add(current_pos)

possible_spots = visited
possible_spots.remove(start_pos) #can't place obstacle where guard is now

loop_count = 0

for test_pos in possible_spots:
    still_testing = True

    current_pos = start_pos
    facing = start_facing

    test_path = set()
    test_path.add((current_pos, facing)) #yes, this is a tuple of type (tuple, int)
    #the facing is important now because if the guard ends up on the same square facing the same direction, she must follow the same path as before and therefore must be in a loop
    #but with a different facing she could cross her previous path and end up somewhere else

    #run the simulation again until either the guard leaves the board, or ends up in a loop
    while still_testing:
        match facing:
            case 0:
                target_pos = (current_pos[0] + 1, current_pos[1])
            case 1:
                target_pos = (current_pos[0], current_pos[1] + 1)
            case 2:
                target_pos = (current_pos[0] - 1, current_pos[1])
            case 3:
                target_pos = (current_pos[0], current_pos[1] - 1)
        if target_pos[0] <= 0 or target_pos[0] > width or target_pos[1] <= 0 or target_pos[1] > height: #if she makes it off the board, she never looped
            still_testing = False
            break
        elif obstacles.get(target_pos, False) or target_pos == test_pos: #add new obstacle without editing obstacle dictionary for the next test
            facing = (facing + 1) % 4
            continue
        else:
            current_pos = target_pos
            if (current_pos, facing) in test_path: #if she's already visited this tile facing this direction, then she must be in a loop
                loop_count += 1
                still_testing = False
                break
            test_path.add((current_pos, facing))

print(loop_count)

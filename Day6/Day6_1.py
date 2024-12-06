#Advent of Code 2024 Day 6 Part 1
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
            current_pos = (x, y)
            visited.add(current_pos)
            facing = 3
        elif j == ">": #this and next 2 are for generality - it would bother me if I didn't have these
            current_pos = (x, y)
            visited.add(current_pos)
            facing = 0
        elif j == "v":
            current_pos = (x, y)
            visited.add(current_pos)
            facing = 1
        elif j == "<":
            current_pos = (x, y)
            visited.add(current_pos)
            facing = 2

height = y
width = x

not_finished = True

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

number_visited = len(visited)
print(number_visited)

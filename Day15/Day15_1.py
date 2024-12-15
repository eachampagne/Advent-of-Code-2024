#Advent of Code Day 15 Part 1
#Solved Dec. 15, 2024

#f = open("minisample.txt")
#f = open("sample.txt")
f = open("input.txt")


# 0: right
# 1: down
# 2: left
# 3: up
def get_neighbor_coor(coor, dir):
    match dir:
        case 0:
            new_coor = (coor[0] + 1, coor[1])
        case 1:
            new_coor = (coor[0], coor[1] + 1)
        case 2:
            new_coor = (coor[0] - 1, coor[1])
        case 3:
            new_coor = (coor[0], coor[1] - 1)
        case _:
            print("invalid direction!")
    return new_coor

reading_instructions = False
instructions = ""

level_map = {} #of form (x, y): int where 1 is a wall and 2 is a box

y = 0
for i in f:
    if i == "\n":
        reading_instructions = True
        continue
    if reading_instructions:
        instructions += i.strip()
    else:
        x = 0
        for j in i:
            match j:
                case "#":
                    level_map[(x, y)] = 1
                case "O":
                    level_map[(x, y)] = 2
                case "@":
                    robot_coor = (x, y)
            x += 1
        y += 1

for i in instructions:
    match i:
        case ">":
            dir = 0
        case "v":
            dir = 1
        case "<":
            dir = 2
        case "^":
            dir = 3
    target_coor = get_neighbor_coor(robot_coor, dir)
    match level_map.get(target_coor, -1):
        case -1: #nothing in space - robot moves without moving boxes
            robot_coor = target_coor
            continue
        case 1: #wall in space - robot doesn't move
            continue
        case 2: #box - have to find out if row of boxes can be used
            final_target = get_neighbor_coor(target_coor, dir)
            boxes_to_shove = 1 #might come in handy for part 2 if the robot can only push a limited number of boxes
            while level_map.get(final_target, -1) == 2:
                #keep looking further out until finding either an open space or a wall
                final_target = get_neighbor_coor(final_target, dir)
                boxes_to_shove += 1

            match level_map.get(final_target, -1):
                case -1: #empty space - robot and boxes move
                    level_map[final_target] = level_map.pop(target_coor)
                    robot_coor = target_coor
                case 1: #wall - nothing happens
                    continue

gps_sum = 0

for i in level_map.keys():
    if level_map[i] == 2:
        gps_sum += i[0] + 100 * i[1]

print(gps_sum)

#Advent of Code Day 15 Part 2
#Solved Dec. 15, 2024

#f = open("minisample.txt")
#f = open("minisample2.txt")
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

#returns which squares border a box in a given direction, regardess of which half of the box you have coordinates for
#if it is vertically lined up with another box, it only returns one coordinate pair
#but otherwise does not check whether the neighboring tiles are boxes, walls, or spaces
def get_boxes_neighbors(coor, dir):
    if level_map[coor] == 2:
        left_half = coor
        right_half = get_neighbor_coor(coor, 0)
    elif level_map[coor] == 3:
        right_half = coor
        left_half = get_neighbor_coor(coor, 2)
    else:
        print("not a box!")
        return
    match dir:
        case 0:
            neighbors = [get_neighbor_coor(right_half, 0)]
        case 1:
            neighbors = [get_neighbor_coor(left_half, 1), get_neighbor_coor(right_half, 1)] 
        case 2:
            neighbors = [get_neighbor_coor(left_half, 2)]
        case 3:
            neighbors = [get_neighbor_coor(left_half, 3), get_neighbor_coor(right_half, 3)] 
    if len(neighbors) == 2:
        if level_map.get(neighbors[0], -1) == 2 and level_map.get(neighbors[1], -1) == 3:
            neighbors = [neighbors[0]] #i.e., if it's one box perfectly lined up, no need to check multiple times
    return neighbors
 
def box_can_move(coor, dir):
    neighbors = get_boxes_neighbors(coor, dir)
    can_move = True
    for i in neighbors:
        match level_map.get(i, -1):
            case -1:
                continue
            case 1:
                can_move = False
            case 2 | 3:
                can_move = can_move and box_can_move(i, dir)
    return can_move

def move_box(coor, dir):
    if level_map[coor] == 2:
        left_half = coor
        right_half = get_neighbor_coor(coor, 0)
    elif level_map[coor] == 3:
        right_half = coor
        left_half = get_neighbor_coor(coor, 2)
    else:
        print("not a box!")
        return
    #move boxes out of the way first or there *will* be problems
    neighbors = get_boxes_neighbors(coor, dir)
    for i in neighbors:
        match level_map.get(i, -1):
            case -1:
                continue
            case 1:
                print("this box shouldn't be able to move!")
            case 2 | 3:
                move_box(i, dir)
    match dir:
        case 0: #right and left - order matters to make certain []'s stay paired
            level_map[get_neighbor_coor(right_half, 0)] = level_map.pop(right_half)
            level_map[get_neighbor_coor(left_half, 0)] = level_map.pop(left_half)
        case 2:
            level_map[get_neighbor_coor(left_half, 2)] = level_map.pop(left_half)
            level_map[get_neighbor_coor(right_half, 2)] = level_map.pop(right_half)
        case 1 | 3: #up and down - order doesn't matter
            level_map[get_neighbor_coor(left_half, dir)] = level_map.pop(left_half)
            level_map[get_neighbor_coor(right_half, dir)] = level_map.pop(right_half)


reading_instructions = False
instructions = ""

level_map = {} #of form (x, y): int where 1 is a wall, 2 is [ (left half of box), and 3 is ] (right half)

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
                    level_map[(x+1, y)] = 1
                case "O":
                    level_map[(x, y)] = 2
                    level_map[(x+1, y)] = 3
                case "@":
                    robot_coor = (x, y)
            x += 2
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
        case 2 | 3: #box - have to find out if row of boxes can be used
            if box_can_move(target_coor, dir):
                move_box(target_coor, dir)
                robot_coor = target_coor
            

#            final_target = get_neighbor_coor(target_coor, dir)
#            boxes_to_shove = 1 #might come in handy for part 2 if the robot can only push a limited number of boxes
#            while level_map.get(final_target, -1) == 2:
#                #keep looking further out until finding either an open space or a wall
#                final_target = get_neighbor_coor(final_target, dir)
#                boxes_to_shove += 1

#            match level_map.get(final_target, -1):
#                case -1: #empty space - robot and boxes move
#                    level_map[final_target] = level_map.pop(target_coor)
#                    robot_coor = target_coor
#                case 1: #wall - nothing happens
#                    continue

gps_sum = 0

for i in level_map.keys():
    if level_map[i] == 2:
        gps_sum += i[0] + 100 * i[1]

print(gps_sum)

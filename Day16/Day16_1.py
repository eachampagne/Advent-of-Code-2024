#Advent of Code 2024 Day 16 Part 1
#Solved Dec. 16, 2024

#I think this might be an application for Dijkstra's algorithm

import queue

def get_neighbors(node):
    coor = node[0]
    facing = node[1]
    match facing:
        case 0:
            forward = ((coor[0]+1, coor[1]), facing)
        case 1:
            forward = ((coor[0], coor[1]+1), facing)
        case 2:
            forward = ((coor[0]-1, coor[1]), facing)
        case 3:
            forward = ((coor[0], coor[1]-1), facing)
        case _:
            print("invalid facing!")
    turn_left = (coor, (facing - 1) % 4)
    turn_right = (coor, (facing + 1) % 4)
    return [forward, turn_left, turn_right]

#f = open("minisample.txt")
#f = open("sample.txt")
f = open("input.txt")

walls = set()

y = 0
for i in f:
    x = 0
    for j in i.strip():
        match j:
            case "#":
                walls.add((x, y))
            case "S":
                start_coor = (x, y)
            case "E":
                end_coor = (x, y)
        x += 1
    y += 1

#facings:
#0 - right/east
#1 - down/south
#2 - left/west
#3 - up/north

initial_facing = 0

starting_node = (start_coor, initial_facing)
starting_cost = 0

to_visit = queue.PriorityQueue()
to_visit.put((starting_cost, starting_node))

visited = {} #of form ((x, y), facing): cost

while not to_visit.empty():
    current = to_visit.get()
    cost = current[0]
    current_node = current[1]
    current_coor = current_node[0]

    if current_node in visited.keys():
        visited[current_node] = min(cost, visited[current_node])
        continue
    else:
        visited[current_node] = cost

    #three neighbors - move forward one tile, rotate CW, rotate CCW
    neighbors = get_neighbors(current_node)
    for i in neighbors:
        neighbor_coor = i[0]
        if neighbor_coor != current_coor:
            if neighbor_coor in walls:
                continue
            else:
                additional_cost = 1
        else:
            additional_cost = 1000
        to_visit.put((cost + additional_cost, i))

final_cost = min(visited[(end_coor, 0)], visited[(end_coor, 1)], visited[(end_coor, 2)], visited[(end_coor, 3)])
print(final_cost)

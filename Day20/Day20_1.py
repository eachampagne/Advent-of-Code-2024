#Advent of Code 2024 Day 20 Part 1
#Solved Dec. 20, 2024

import queue

def get_neighbors(coor, width, height):
    neighbors = []
    x = coor[0]
    y = coor[1]
    if x - 1 >= 0:
        neighbors.append((x-1, y))
    if x + 1 < width:
        neighbors.append((x+1, y))
    if y - 1 >= 0:
        neighbors.append((x, y-1))
    if y + 1 < height:
        neighbors.append((x, y+1))
    return neighbors

#f = open("sample.txt")
f = open("input.txt")

paths = set() #there seems to be more walls than paths

y = 0
for i in f:
    x = 0
    for j in i.strip():
        match j:
            case "S":
                start_coor = (x, y)
                paths.add((x, y))
            case "E":
                end_coor = (x, y)
                paths.add((x, y))
            case ".":
                paths.add((x, y))
        x += 1
    y += 1

width = x
height = y



to_visit = queue.Queue()
to_visit.put(start_coor)

visited = []

no_steps = {}
no_steps[start_coor] = 0

while not to_visit.empty():
    current_tile = to_visit.get()
    visited.append(current_tile)
    current_steps = no_steps[current_tile]

    for neighbor in get_neighbors(current_tile, width, height):
        if neighbor in paths:
            if neighbor not in visited:
                to_visit.put(neighbor)
                no_steps[neighbor] = current_steps + 1

shortcut_quantities = {} #form length: quantity
for i in visited:
    neighbors = get_neighbors(i, width, height)
    for j in neighbors:
        if j not in paths:
            neighbors_2nd_degree = get_neighbors(j, width, height)
            for k in neighbors_2nd_degree:
                if k in paths:
                    shortcut_length = no_steps[k] - no_steps[i] - 2
                    if shortcut_length > 0:
                        shortcut_quantities[shortcut_length] = shortcut_quantities.get(shortcut_length, 0) + 1

#print(shortcut_quantities)

no_good_shortcuts = 0

for i in shortcut_quantities.keys():
    if i >= 100:
        no_good_shortcuts += shortcut_quantities[i]

print(no_good_shortcuts)

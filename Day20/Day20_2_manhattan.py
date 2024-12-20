#Advent of Code 2024 Day 20 Part 2
#Solved Dec. 20, 2024

#A (hopefully) more efficient solve based on other people's solutions
#My first solve worked but was pretty inefficient. Now that I've looked at other people's comments I'm going to back to my original idea of using entry/exit pairs, but rather than BFSing for a valid path I can just check that the Manhattan distance is less than 20.
#This takes only a few seconds
#I wish I'd thought of this myself!

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

def manhattan_dist(coor1, coor2):
    x1 = coor1[0]
    y1 = coor1[1]
    x2 = coor2[0]
    y2 = coor2[1]
    return abs(y2-y1) + abs(x2-x1)

do_real_input = True

if do_real_input:
    f = open("input.txt")
    good_shortcut_cutoff = 100
else:
    f = open("sample.txt")
    good_shortcut_cutoff = 50

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

shortcut_max_steps = 20

no_good_shortcuts = 0

for i in range(len(visited)):
    shortcut_start = visited[i]
    for j in range(i+1, len(visited)):
        shortcut_end = visited[j]
        dist = manhattan_dist(shortcut_start, shortcut_end)
        time_saved = no_steps[shortcut_end] - no_steps[shortcut_start] - dist
        if dist <= shortcut_max_steps and time_saved >= good_shortcut_cutoff:
            no_good_shortcuts += 1

print(no_good_shortcuts)

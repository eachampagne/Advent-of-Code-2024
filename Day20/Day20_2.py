#Advent of Code 2024 Day 20 Part 2
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

shortcut_quantities = {} #form length: quantity
shortcut_max_steps = 20

best_shortcuts = {} #form (start, end): number of steps saved

#This BFS-expands from every point along the path out to a distance of 20. Within this space, every tile that is also a path calculates the benefit of the shortcut between them
#At first I tried calculating shortcuts from every entry/exit path, then realized I was computing the same BFS over and over again
#This is much better. It still takes about 3 minutes to run, so it could probably be optimized, but it does the job in a time I'm willing to wait for
for i in range(len(visited)):
    shortcut_start = visited[i]

    shortcut_to_visit = queue.Queue()
    shortcut_to_visit.put(shortcut_start)
    steps_in_shortcut = {shortcut_start: 0}

    shortcut_visited = []

    while not shortcut_to_visit.empty():
        current_shortcut_tile = shortcut_to_visit.get()
        if current_shortcut_tile in shortcut_visited:
            continue
        shortcut_visited.append(current_shortcut_tile)
        current_step = steps_in_shortcut[current_shortcut_tile]
        next_step = current_step + 1
        if next_step > shortcut_max_steps:
            continue
        for neighbor in get_neighbors(current_shortcut_tile, width, height):
            shortcut_to_visit.put(neighbor)
            steps_in_shortcut[neighbor] = min(steps_in_shortcut.get(neighbor, shortcut_max_steps + 1), next_step)
            if neighbor in paths:
                steps_saved = no_steps[neighbor] - no_steps[shortcut_start] - next_step
                best_shortcuts[(shortcut_start, neighbor)] = max(best_shortcuts.get((shortcut_start, neighbor), 0), steps_saved)

no_good_shortcuts = 0

for i in best_shortcuts.keys():
    if best_shortcuts[i] >= good_shortcut_cutoff:
        no_good_shortcuts += 1

print(no_good_shortcuts)

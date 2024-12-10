#Advent of Code 2024 Day 10 Part 1
#Solved Dec. 10, 2024

import queue

#f = open("sample.txt")
f = open("input.txt")

grid = []
trailheads = []
peaks = []

#  ----> x
# |
# |
# |
# |
# v y

def taxi_dist(coor_1, coor_2): #(int, int), (int, int)
    return abs(coor_2[0] - coor_1[0]) + abs(coor_2[1] - coor_1[1])

def get_neighbors(coor, width, height): #(int, int), int, int
    neighbors = []
    if coor[0] - 1 >= 0:
        neighbors.append((coor[0]-1, coor[1]))
    if coor[0] + 1 < width:
        neighbors.append((coor[0]+1, coor[1]))
    if coor[1] - 1 >= 0:
        neighbors.append((coor[0], coor[1]-1))
    if coor[1] + 1 < height:
        neighbors.append((coor[0], coor[1]+1))
    return neighbors

y = 0
for i in f:
    row = []
    x = 0
    for j in i.strip():
        row.append(int(j))
        if int(j) == 0:
            trailheads.append((x, y))
        if int(j) == 9:
            peaks.append((x, y))
        x += 1
    grid.append(row)
    y += 1

map_width = len(grid[0]) #assumes that grid is rectangular
map_height = len(grid)

score_sum = 0

for i in trailheads:
    can_reach = set()

    to_search = queue.Queue()
    visited = set()

    to_search.put(i)

    while not to_search.empty():
        current_tile = to_search.get()
        if current_tile in visited:
            continue
        current_height = grid[current_tile[1]][current_tile[0]]
        if current_height == 9:
            can_reach.add(current_tile)
            continue
        neighbors = get_neighbors(current_tile, map_width, map_height)
        for neighbor in neighbors:
            height = grid[neighbor[1]][neighbor[0]]
            if height == current_height + 1:
                to_search.put(neighbor)
        visited.add(current_tile)
    
    score_sum += len(can_reach)

print(score_sum)

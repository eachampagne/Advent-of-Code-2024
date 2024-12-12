#Advent of Code 2024 Day 12 Part 1
#Solved Dec. 12, 2024

from queue import Queue

def get_neighbors(coor, width, height):
    neighbors = []
    if coor[0] - 1 >= 0:
        neighbors.append((coor[0] - 1, coor[1]))
    if coor[0] + 1 < width:
        neighbors.append((coor[0] + 1, coor[1]))
    if coor[1] - 1 >= 0:
        neighbors.append((coor[0], coor[1] - 1))
    if coor[1] + 1 < height:
        neighbors.append((coor[0], coor[1] + 1))
    return neighbors

#in the while loop, I count perimeter by incrementing every time a tile neighbors a tile of a different plant type
#but this misses all the perimeter at the edge of the grid, where there is no neighbor to check
def get_edge_perimeter(coor, width, height):
    edge = 0
    if coor[0] - 1 < 0:
        edge += 1
    if coor[0] + 1 >= width:
        edge += 1
    if coor[1] - 1 < 0:
        edge += 1
    if coor[1] + 1 >= height:
        edge += 1
    return edge

#f = open("tinysample.txt")
#f = open("minisample.txt")
#f = open("sample.txt")
f = open("input.txt")

grid = []

for i in f:
    grid.append(i.strip())

grid_height = len(grid)
grid_width = len(grid[0])

#There will be 2 queues - one for plants that match to find everything in a given region
#and one for other types of plants to start checking the next region when the current one is finished
to_search_later = Queue()
visited = set()

to_search_later.put((0,0)) #start at top left

total_cost = 0

while not to_search_later.empty():
    region_start_tile = to_search_later.get() #to_search_later tracks tiles from one region seen from another
    #it allows moving to a new region once finished a previous one

    if region_start_tile in visited:
        continue

    perimeter = 0
    area = 0

    plant_type = grid[region_start_tile[1]][region_start_tile[0]]
    
    to_search = Queue()
    to_search.put(region_start_tile)

    while not to_search.empty():
        current_tile = to_search.get()
        if current_tile in visited:
            continue

        area += 1
        perimeter += get_edge_perimeter(current_tile, grid_width, grid_height)
        
        neighbors = get_neighbors(current_tile, grid_width, grid_height)

        for i in neighbors:
            neighbor_plant = grid[i[1]][i[0]]
            if neighbor_plant == plant_type:
                to_search.put(i)
            else: #if plant types don't match, there's perimeter between them
                perimeter += 1
                to_search_later.put(i)

        visited.add(current_tile)

    region_cost = perimeter * area
    total_cost += region_cost

print(total_cost)

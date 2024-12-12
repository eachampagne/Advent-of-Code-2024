#Advent of Code 2024 Day 12 Part 2
#Solved Dec. 12, 2024

from queue import Queue

#coordinates for the fenceposts are on the dual to the plots themselves
#the coordinate of the top-left post matches the coordinate of a given plot
#this means that fencepost coordinates will start at (0, 0) and go to (width, height)

#a given fence segment is defined as (coor, coor) or ((int, int), (int, int)), ordered left to right as if you're standing in the plot looking across the fence into the neighboring plot of a different region
#all fences should "flow" clockwise about a region
#this will maintain the "sidedness" (inside vs outside) of the fence

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
#function revised and renamed to get edge segments along the grid boundary to be combined into sides
def get_boundary_edges(coor, width, height):
    x = coor[0]
    y = coor[1]

#   (x, y)--------(x+1, y)
#     |               |
#     |    (x, y)     |
#     |               |
#   (x, y+1)------(x+1, y+1)

    edges = []
    if x - 1 < 0:
        edges.append(((x, y+1), (x, y)))
    if x + 1 >= width:
        edges.append(((x+1, y),(x+1, y+1)))
    if y - 1 < 0:
        edges.append(((x, y), (x+1, y)))
    if y + 1 >= height:
        edges.append(((x+1, y+1), (x, y+1)))
    return edges

#get edge between two adjacent tiles
def get_edge_between(coor1, coor2):
    x1 = coor1[0]
    y1 = coor1[1]
    x2 = coor2[0]
    y2 = coor2[1]

    delta = ((x2-x1), (y2-y1))
    match delta:
        case (1, 0):
            return ((x2, y1),(x2, y1+1))
        case (-1, 0):
            return ((x1, y1+1),(x1, y1))
        case (0, 1):
            return ((x1+1, y2),(x1, y2))
        case (0, -1):
            return ((x1, y1),(x1+1, y1))
        case _:
            print("tiles are not adjacent!")

#get direction of side
#doing this as a vector would give different vector lengths for different side lengths, which complicatescomparisons
#so an integer represents each direction
# 0: left -> right
# 1: top -> bottom
# 2: right -> left
# 3: bottom -> top
def side_direction(side):
    x1 = side[0][0]
    y1 = side[0][1]
    x2 = side[1][0]
    y2 = side[1][1]

    if x1 == x2:
        if y1 > y2:
            return 3
        elif y2 > y1:
            return 1
        else:
            print("invalid side: both coordinates equal")
            print(side)
    elif y1 == y2:
        if x1 > x2:
            return 0
        elif x2 > x1:
            return 2
        else:
            print("invalid side: both coordinates equal")
            print(side)
    else:
        print("invalid side: posts are not in a straight line")
        print(side)

#this doesn't cover cases where one side encompasses the other... but that shouldn't come up since each fence segment should only get found once
def can_combine_sides(side1, side2):
    if side_direction(side1) == side_direction(side2): #need to be in the same direction
        if side1[1] == side2[0] or side2[1] == side1[0]: #must have a shared corner
            return True
    return False

def combine_sides(side1, side2):
    if not can_combine_sides(side1, side2):
        print("these sides can't go together!")
    if side1[1] == side2[0]:
        return (side1[0], side2[1])
    elif side2[1] == side1[0]:
        return (side2[0], side1[1])
    else:
        print("problem with combining!")

#f = open("tinysample.txt")
#f = open("minisample.txt")
#f = open("esample.txt")
#f = open("absample.txt")
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

    sides = [[], [], [], []] #sorting the sides by direction means fewer things to check
    area = 0

    plant_type = grid[region_start_tile[1]][region_start_tile[0]]
    
    to_search = Queue()
    to_search.put(region_start_tile)

    while not to_search.empty():
        current_tile = to_search.get()
        if current_tile in visited:
            continue

        area += 1
        boundary_edges = get_boundary_edges(current_tile, grid_width, grid_height)

        for i in boundary_edges:
            side_to_sort = i
            direction = side_direction(side_to_sort)
            for j in range(len(sides[direction])-1, -1, -1): #count backwards so popping two different ones won't break anything
                side_to_compare = sides[direction][j]
                if can_combine_sides(side_to_sort, side_to_compare):
                    side_to_sort = combine_sides(side_to_sort, side_to_compare) #this should allow connecting to two different existing sides
                    sides[direction].pop(j) #get rid of old side that's being combined
            sides[direction].append(side_to_sort)

        neighbors = get_neighbors(current_tile, grid_width, grid_height)

        for i in neighbors:
            neighbor_plant = grid[i[1]][i[0]]
            if neighbor_plant == plant_type:
                to_search.put(i)
            else: #if plant types don't match, there's perimeter between them
                side_to_sort = get_edge_between(current_tile, i)
                direction = side_direction(side_to_sort)
                for j in range(len(sides[direction])-1, -1, -1): #count backwards so popping two different ones won't break anything
                    side_to_compare = sides[direction][j]
                    if can_combine_sides(side_to_sort, side_to_compare):
                        side_to_sort = combine_sides(side_to_sort, side_to_compare) #this should allow connecting to two different existing sides
                        sides[direction].pop(j) #get rid of old side that's being combined
                sides[direction].append(side_to_sort)
                
                to_search_later.put(i)

        visited.add(current_tile)
    
    #the sides are sorted by direction, so need to add them all up
    no_sides = 0
    for i in sides:
        no_sides += len(i)

    region_cost = no_sides * area
    total_cost += region_cost

print(total_cost)

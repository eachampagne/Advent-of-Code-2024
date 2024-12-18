#Advent of Code Day 18 Part 2
#Solved Dec. 18, 2024

#Trying an alternative solution -  keep track of my current best path, and update when a new byte landed on that path
#This is actually slower than the binary search solution - probably because it has to calculate new paths more times. But the binary search was easier to implement, so I felt like I was cheating and that the path tracking was the "better" way. Turns out it wasn't - now I know.
#There probably are algorithms for trying to update a small part of a path rather than recalculating the whole thing from scratch. That might be faster except in extreme cases where a shortcut gets closed off and you have to totally reroute. I don't know how to implement that though.

from queue import Queue

def get_neighbors(coor, width, height):
    x = coor[0]
    y = coor[1]
    neighbors = []
    if x-1 >= 0:
        neighbors.append((x-1, y))
    if x+1 < width:
        neighbors.append((x+1, y))
    if y-1 >= 0:
        neighbors.append((x, y-1))
    if y+1 < height:
        neighbors.append((x, y+1))
    return neighbors

do_real_input = True

start_coor = (0, 0)

if do_real_input:
    f = open("input.txt")
    starting_byte = 1024
    width = 71
    height = 71
    exit_coor = (70, 70)
else:
    f = open("sample.txt")
    starting_byte = 12
    width = 7
    height = 7
    exit_coor = (6, 6)

corrupted_ever = []

for i in f:
    coor = tuple(map(int, i.split(",")))
    corrupted_ever.append(coor)

corrupted = set(corrupted_ever[:starting_byte+1])
new_byte_index = starting_byte

passable = True

current_best_path = set()
calc_new_path = True

while passable:
    new_byte_index += 1
    new_byte = corrupted_ever[new_byte_index]

    corrupted.add(new_byte)
    if new_byte in current_best_path:
        calc_new_path = True

    if calc_new_path:
        to_visit = Queue()
        to_visit.put((start_coor, start_coor))

        visited = {} #this is now of form node: parent
    
        path_found = False

        while not to_visit.empty():
            node = to_visit.get()
            current_coor = node[0]
            parent = node[1]
            if current_coor in visited:
                continue
            visited[current_coor] = parent
            if current_coor == exit_coor:
                #path found - this still works
                path_found = True
                current_best_path = set()
                parent_node = parent
                path_node = current_coor
                while path_node != start_coor:
                    current_best_path.add(visited[path_node])
                    path_node = parent_node
                    parent_node = visited[parent_node]
                calc_new_path = False
                break

            neighbors = get_neighbors(current_coor, width, height)

            for i in neighbors:
                if i not in corrupted:
                    to_visit.put((i, current_coor))

        if not path_found:
            #to_visit emptied without finding exit - path is blocked
            passable = False

            final_byte_string = str(new_byte[0]) + "," + str(new_byte[1])
            print(final_byte_string)

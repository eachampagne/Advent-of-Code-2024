#Advent of Code 2024 Day 14 Part 1
#Solved Dec. 14, 2024

do_sample = False

if do_sample:
    f = open("sample.txt")
    width = 11
    height = 7
else:
    f = open("input.txt")
    width = 101
    height = 103

no_seconds = 100
quadrants_count = [0, 0, 0, 0] 

horiz_line = int((height - 1) / 2) #the y coordinate that divides the quadrants
vert_line = int((width - 1) / 2) #the x coordinate that divides the quadrants
# Robots with these final coordinates don't count

for i in f:
    data = i.split()
    start_pos = list(map(int, data[0].split("=")[1].split(",")))
    velocity = list(map(int, data[1].split("=")[1].split(",")))
    
    final_x = (start_pos[0] + no_seconds * velocity[0]) % width
    final_y = (start_pos[1] + no_seconds * velocity[1]) % height

    if final_x < vert_line and final_y < horiz_line:
        quadrants_count[0] += 1
    elif final_x > vert_line and final_y < horiz_line:
        quadrants_count[1] += 1
    elif final_x < vert_line and final_y > horiz_line:
        quadrants_count[2] += 1
    elif final_x > vert_line and final_y > horiz_line:
        quadrants_count[3] += 1

safety_factor = 1

for i in quadrants_count:
    safety_factor *= i

print(safety_factor)

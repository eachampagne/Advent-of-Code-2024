#Advent of Code 2024 Day 21 Part 2
#Solved Dec. 21, 2024

#Another solve thanks to memoization!
#Changes: add a memo dictionary that tracks solutions for keys of form (starting_key, ending_key, iteration)
#Adds checking/updating the memo dictionary to the find_number_presses function
#Adds a target_depth parameter to find_number_presses so it's less of a magic number
#Changes the final iteration from 3 to 26 via new target_depth parameter

from enum import Enum

class Keys_Num(Enum):
    ZERO = 0
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    A = 10

keypad_num = {
    (0, 0): Keys_Num.SEVEN,
    (1, 0): Keys_Num.EIGHT,
    (2, 0): Keys_Num.NINE,
    (0, 1): Keys_Num.FOUR,
    (1, 1): Keys_Num.FIVE,
    (2, 1): Keys_Num.SIX,
    (0, 2): Keys_Num.ONE,
    (1, 2): Keys_Num.TWO,
    (2, 2): Keys_Num.THREE,
    (1, 3): Keys_Num.ZERO,
    (2, 3): Keys_Num.A
}

class Keys_Dir(Enum):
    A = 0
    UP = 1
    LEFT = 2
    DOWN = 3
    RIGHT = 4

keypad_dir = {
    (1, 0): Keys_Dir.UP,
    (2, 0): Keys_Dir.A,
    (0, 1): Keys_Dir.LEFT,
    (1, 1): Keys_Dir.DOWN,
    (2, 1): Keys_Dir.RIGHT
}

def add_coors(coor, coor_to_add):
    return (coor[0] + coor_to_add[0], coor[1] + coor_to_add[1])

#I'm going to assume that any path that changes direction more than once is suboptimal, so the only options would be to go horizontal first or vertical first. If either path hits the missing key, it's invalid
def generate_paths(start_coor, end_coor, missing):
    go_right = (end_coor[0] >= start_coor[0])
    left_right_presses = abs(end_coor[0] - start_coor[0]) #pos is right, neg is left 
    go_down = (end_coor[1] >= start_coor[1])
    up_down_presses = abs(end_coor[1] - start_coor[1]) #pos is down, neg is up
    path_1 = []
    path_2 = []
    for i in range(left_right_presses):
        path_1.append(Keys_Dir.RIGHT if go_right else Keys_Dir.LEFT)
        path_2.append(Keys_Dir.RIGHT if go_right else Keys_Dir.LEFT)
    for i in range(up_down_presses):
        path_1.append(Keys_Dir.DOWN if go_down else Keys_Dir.UP)
        path_2.insert(0, Keys_Dir.DOWN if go_down else Keys_Dir.UP)
    path_1.append(Keys_Dir.A)
    path_2.append(Keys_Dir.A)
    if path_1 == path_2: #cases where you only move along one dimension, or stay in the same spot (repeated key presses)
        paths = [path_1]
        return paths
    #check for missing key - path 1
    key_path_i = start_coor
    for i in path_1:
        match i:
            case Keys_Dir.UP:
                key_path_i = add_coors(key_path_i, (0, -1))
            case Keys_Dir.DOWN:
                key_path_i = add_coors(key_path_i, (0, 1))
            case Keys_Dir.LEFT:
                key_path_i = add_coors(key_path_i, (-1, 0))
            case Keys_Dir.RIGHT:
                key_path_i = add_coors(key_path_i, (1, 0))
        if key_path_i == missing:
            paths = [path_2]
            return paths
    #check for missing key - path 2
    key_path_i = start_coor
    for i in path_2:
        match i:
            case Keys_Dir.UP:
                key_path_i = add_coors(key_path_i, (0, -1))
            case Keys_Dir.DOWN:
                key_path_i = add_coors(key_path_i, (0, 1))
            case Keys_Dir.LEFT:
                key_path_i = add_coors(key_path_i, (-1, 0))
            case Keys_Dir.RIGHT:
                key_path_i = add_coors(key_path_i, (1, 0))
        if key_path_i == missing:
            paths = [path_1]
            return paths
    paths = [path_1, path_2]
    return paths

def find_number_presses(starting_key, ending_key, iteration, target_depth):
    if (starting_key, ending_key, iteration) in memo:
        return memo[(starting_key, ending_key, iteration)]
    if iteration == target_depth:
        return 1
    if iteration == 0:
        keypad_dict = keypad_num
        missing = (0, 3)
        #starting_key = Keys_Num.A
    else:
        keypad_dict = keypad_dir
        missing = (0, 0)
        #starting_key = Keys_Dir.A
    for i in keypad_dict.items():
        if i[1] == starting_key:
            start_coor = i[0]
        if i[1] == ending_key:
            end_coor = i[0]
    paths = generate_paths(start_coor, end_coor, missing)
    presses_per_path = [] #an array that tracks the sum of the returns of find_number_presses_directional for each proposed path
    for i in paths:
        #print(i)
        presses = 0
        current_key = Keys_Dir.A
        for j in i:
            next_key = j
            presses += find_number_presses(current_key, next_key, iteration + 1, target_depth)
            current_key = next_key
        presses_per_path.append(presses)
    answer = min(presses_per_path)
    memo[(starting_key, ending_key, iteration)] = answer
    return answer

memo = {}

###############

#f = open("sample.txt")
f = open("input.txt")

complexity = 0
for i in f:
    code = i.strip()
    numeric = int(code[:-1])
    starting_key = Keys_Num.A
    length = 0
    for j in code:
        match j:
            case "0":
                ending_key = Keys_Num.ZERO
            case "1":
                ending_key = Keys_Num.ONE
            case "2":
                ending_key = Keys_Num.TWO
            case "3":
                ending_key = Keys_Num.THREE
            case "4":
                ending_key = Keys_Num.FOUR
            case "5":
                ending_key = Keys_Num.FIVE
            case "6":
                ending_key = Keys_Num.SIX
            case "7":
                ending_key = Keys_Num.SEVEN
            case "8":
                ending_key = Keys_Num.EIGHT
            case "9":
                ending_key = Keys_Num.NINE
            case "A":
                ending_key = Keys_Num.A
        length += find_number_presses(starting_key, ending_key, 0, 26)
        starting_key = ending_key
    complexity += numeric * length

print(complexity)
                


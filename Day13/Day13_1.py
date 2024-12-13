#Advent of Code 2024 Day 13 Part 1
#Solved Dec. 13, 2024

from math import isclose

#f = open("sample.txt")
f = open("input.txt")

button_a = []
button_b = []
prize = []

for i in f:
    if i == "\n":
        continue
    data = i.split(":")
    coords_str = list(map(str.strip, data[1].split(","))) #gets each X+###, Y=### parts
    if data[0] == "Button A":
        coords = list(map(int, [i.split("+")[1] for i in coords_str])) #this is incredibly ugly
        #I wouldn't use this mess in anything I needed to work reliably for more than one day
        #but for the purpose of an AOC script that just has to work once, it's a good way to practice some of these syntax features I don't use often
        button_a.append(coords)
    elif data[0] == "Button B":
        coords = list(map(int, [i.split("+")[1] for i in coords_str]))
        button_b.append(coords)
    elif data[0] == "Prize":
        coords = list(map(int, [i.split("=")[1] for i in coords_str]))
        prize.append(coords)

no_tokens = 0

#...Numpy would make this easier, but I only want to use the standard libraries
def inverse(matrix):
    #matrix is [[a, b], 
    #           [c, d]] 
    a = matrix[0][0]
    b = matrix[0][1]
    c = matrix[1][0]
    d = matrix[1][1]

    det = a*d - b*c

    new_matrix = [[d/det, -b/det], [-c/det, a/det]]
    return new_matrix

def matrix_mul(matrix, vec):
    a = matrix[0][0]
    b = matrix[0][1]
    c = matrix[1][0]
    d = matrix[1][1]

    x = vec[0]
    y = vec[1]

    new_vec = [a*x+b*y, c*x+d*y]
    return new_vec

def create_matrix(a, b, c, d):
    # [[a, b],
    #  [c, d]]
    return [[a, b], [c, d]]

#this is a linear algebra problem

# the way this works is
# position as a function of button presses is:

# [final position x   = [A units x     B units x     * [A presses
#  final position y]     A units y     B units y]       B presses] 

# so to get button presses in terms of the target position:

# [A presses   = [A units x     B units x   ^-1  * [target x
#  B presses]     A units y     B units y  ]        target y] 

#this also means that, provided that the two buttons are linearly independent, there is a unique way to get to each target position
#it's just a matter of checking whether that solution has integer button presses
#so optimizing for cost isn't an issue because there aren't multiple solutions
#...provided they're linearly independent
#which I did not test for, but it worked anyway
#if I hadn't gotten the right answer that would have been the first thing I checked
for a_vec, b_vec, p_vec in zip(button_a, button_b, prize):
    transformation_matrix = inverse(create_matrix(a_vec[0], b_vec[0], a_vec[1], b_vec[1]))
    button_press_vec = matrix_mul(transformation_matrix, p_vec)
    button_press_int = list(map(round, button_press_vec))

    tokens = 0

    #have to use isclose to compensate for division precision
    if isclose(button_press_vec[0], button_press_int[0]) and isclose(button_press_vec[1], button_press_int[1]):
        tokens  = 3*button_press_int[0] + button_press_int[1]

    no_tokens += tokens

print(no_tokens)

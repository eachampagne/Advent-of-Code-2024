#Advent of Code 2024 Day 24 Part 1
#Solved Dec. 24, 2024

from enum import Enum

def perform_op(input_1, input_2, operation):
    match operation:
        case op.AND:
            return input_1 and input_2
        case op.OR:
            return input_1 or input_2
        case op.XOR:
            return input_1 ^ input_2

def solve_wire(wire):
    presolved = wire_values.get(wire, -1)
    if presolved != -1:
        return presolved
    rule = wire_rules[wire]
    input_1 = rule[0][0]
    input_2 = rule[0][1]
    operation = rule[1]
    answer = perform_op(solve_wire(input_1), solve_wire(input_2), operation)
    wire_values[wire] = answer
    return answer

#f = open("minisample.txt")
#f = open("sample.txt")
f = open("input.txt")

wire_values = {}
wire_rules = {}

class op(Enum):
    AND = 0
    OR = 1
    XOR = 2

highest_z = -1

reading_inputs = True
for i in f:
    if i == "\n":
        reading_inputs = False
        continue
    if reading_inputs:
        wire_input = i.split()
        wire = wire_input[0][:-1] #drop the colon
        value = int(wire_input[1])
        wire_values[wire] = value
    else:
        rule = i.split()
        result = rule[-1]
        if result[0] == "z":
            z_value = int(result[1:])
            highest_z = max(highest_z, z_value)
        input_1 = rule[0]
        input_2 = rule[2] #input order doesn't actually matter for any of these operations
        match rule[1]:
            case "AND":
                operation = op.AND
            case "OR":
                operation = op.OR
            case "XOR":
                operation = op.XOR
        wire_rules[result] = ((input_1, input_2), operation)

solution = 0
for i in range(1, highest_z+1):
    wire_to_calc = "z" + str(i).zfill(2) #have to pad to 2 digits
    solved_wire = solve_wire(wire_to_calc)
    solution += solved_wire * 2**i

print(solution)

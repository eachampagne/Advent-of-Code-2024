#Advent of Code 2024 Day 24 Part 2
#Solved Dec. 24, 2024

#This isn't really good... a bunch of ad hoc tests until I hit 8 reported errors
#In theory you could build up the lists of carries and half carries to follow the full chain of logic
#It does seem like my input was fairly nice
#There should be several ways to compute the carry, but it was consistent about it
#I did a bunch of hand checking to validate the errors it spat out
#This isn't elegant, there's unused code everywhere from when I was more ambitious, and the code has no way to figure out which errors are paired with each other
#But it got me to the answer and I got my star
#I'd like to say I'm going to clean this one up later, but I'm probably not

from enum import Enum

def perform_op(input_1, input_2, operation):
    match operation:
        case op.AND:
            return input_1 and input_2
        case op.OR:
            return input_1 or input_2
        case op.XOR:
            return input_1 ^ input_2

#returns true if wires are equivalent, even with reversed inputs, false otherwise
def wires_same_or_flipped(wire_1, wire_2):
    inputs_1 = wire_1[0]
    op_1 = wire_1[1]
    inputs_2 = wire_2[0]
    op_2 = wire_2[1]
    if op_1 == op_2 and (inputs_1 == inputs_2 or inputs_1 == (inputs_2[1], inputs_2[0])):
        return True
    else:
        return False

def solve_wire(wire):
    if wire[0] == "x" or wire[0] == "y": #x's and y's are the inputs to the whole circuits and should never depend on previous wires
        return wire_values[wire]
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
rules_by_id = {}
used_in = {}
rule_id_to_result = {}

inputs_xor = {}
inputs_and = {}
carries = {}
half_carries = {}

half_carry_wire_names = {} #this maps half_carry_n to the wire name it should produce
carry_wire_names = {}

class op(Enum):
    AND = 0
    OR = 1
    XOR = 2

highest_z = -1

incorrect = set()
z_outputs_to_sort = []
half_carries_to_sort = []
carries_to_sort = []

rule_id = 0
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
        rules_by_id[rule_id] = ((input_1, input_2), operation)
        used_in[input_1] = used_in.get(input_1, []) + [rule_id]
        used_in[input_2] = used_in.get(input_2, []) + [rule_id]

        if input_1[0] == "x" or input_1[0] == "y":
            #there are a lot of assumptions here about my input data being what I expect
            #for instance, that the only rules that take in the x and y data will be of 1 of 2 forms:
            #    x## XOR y##
            #    x## AND y##
            #where the numbers always match, though the positions of x and y can be swapped
            input_number = int(input_1[1:])
            if operation == op.XOR:
                inputs_xor[input_number] = rule_id
            if operation == op.AND:
                inputs_and[input_number] = rule_id
        else:
            match operation:
                case op.XOR:
                    z_outputs_to_sort.append(rule_id)
                    if result[0] != "z":
                        incorrect.add(result) #because it's a non-input XOR that doesn't lead to an output
                case op.AND:
                    half_carries_to_sort.append(rule_id)
                case op.OR:
                    carries_to_sort.append(rule_id)
            if result[0] == "z" and operation != op.XOR:
                incorrect.add(result) #only XOR ops can lead to output

        rule_id_to_result[rule_id] = result
        rule_id += 1

incorrect.remove("z" + str(highest_z).zfill(2)) #last bit is irregular

#z_n = (x_n XOR y_n) XOR carry_n-1 (except for 00 case)
#half_carry_n = (x_n-1 XOR y_n-1) AND carry_n-1
#carry_n = (x_n-1 AND y_n-1) OR half_carry_n

#validate the xn XOR/AND yn rules while building the half_carry, carry, and z output lists
for i in range(highest_z): #there are 1 fewer x/y bits than z bits
    xor_id = inputs_xor[i]
    and_id = inputs_and[i]
    xor_result = rule_id_to_result[xor_id]
    and_result = rule_id_to_result[and_id]
    if i == 0:
        if xor_result != "z00":
            incorrect.add(xor_result)
    elif xor_result[0] == "z":
        incorrect.add(xor_result)
    else:   
        for rule_id in used_in[xor_result]:
            dependent_rule = rules_by_id[rule_id]
            operation = dependent_rule[1]
            other_term = dependent_rule[0][1] if dependent_rule[0][0] == xor_result else dependent_rule[0][0]
            match operation:
                case op.XOR:
                    pass
                case op.AND:
                    pass
                case op.OR:
                    incorrect.add(xor_result) #because it's an X^Y that gets used by an OR
    if i == 0:
        #carry_wire_names[i] = and_result
        carries[0] = and_id
    elif and_result[0] == "z":
        incorrect.add(and_result) #because it's an X&Y that leads to output
    else:
        for rule_id in used_in[and_result]:
            dependent_rule = rules_by_id[rule_id]
            operation = dependent_rule[1]
            other_term = dependent_rule[0][1] if dependent_rule[0][0] == xor_result else dependent_rule[0][0]
            match operation:
                case op.OR:
                    half_carry_wire_names[i] = other_term
                    carries[i] = rule_id
                case op.AND:
                    incorrect.add(and_result) #because it's an X&Y that gets used by an AND")
                case op.XOR:
                    incorrect.add(and_result) #because it's an X&Y that gets used by an XOR")

incorrect_list = list(incorrect)
incorrect_list.sort()
final_string = incorrect_list[0]
for i in range(1, len(incorrect_list)):
    final_string += "," + incorrect_list[i]

print(final_string)

#Advent of Code 2024 Day 11 Part 1
#Solved Dec. 11, 2024

#f = open("sample.txt")
f = open("input.txt")

def get_length(number, current_depth, target_depth):
    if current_depth >= target_depth: #check for off-by-one errors
        return 1
    if number == 0:
        return get_length(1, current_depth + 1, target_depth)
    elif len(str(number)) % 2 == 0:
        number_string = str(number)
        string_length = len(number_string)
        first_half = int(number_string[:int(string_length/2)])
        second_half = int(number_string[int(string_length/2):])
        return get_length(first_half, current_depth + 1, target_depth) + get_length(second_half, current_depth + 1, target_depth)
    else:
        return get_length(number * 2024, current_depth + 1, target_depth)

no_rocks = 0

for i in f:
    numbers = list(map(int, i.split()))
    for j in numbers:
        no_rocks += get_length(j, 0, 25)

print(no_rocks)

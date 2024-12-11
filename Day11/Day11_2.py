#Advent of Code 2024 Day 11 Part 2
#Solved Dec. 11, 2024

#f = open("sample.txt")
f = open("input.txt")

#treated as a global variable
lookup = {} #form (number, depth_to_go): length

#So glad I made target_depth a variable instead of a magic number
#And yet it's still not good enough on its own
#made a lookup table to cut down on repeated calculations
#glad someone mentioned dynamic programming on the subreddit a couple days ago or I don't know if I'd have thought of this
#I think this is an example of memoization, which is only one aspect of dynamic programming
#I guess that's a topic I should look more into
def get_length(number, current_depth, target_depth):
    if current_depth >= target_depth: #check for off-by-one errors
        return 1
    else:
        depth_diff = target_depth - current_depth
    if (number, depth_diff) in lookup:
        return lookup[(number, depth_diff)]
    elif number == 0:
        answer =  get_length(1, current_depth + 1, target_depth)
    elif len(str(number)) % 2 == 0:
        number_string = str(number)
        string_length = len(number_string)
        first_half = int(number_string[:int(string_length/2)])
        second_half = int(number_string[int(string_length/2):])
        answer = get_length(first_half, current_depth + 1, target_depth) + get_length(second_half, current_depth + 1, target_depth)
    else:
        answer = get_length(number * 2024, current_depth + 1, target_depth)
    lookup[(number, depth_diff)] = answer
    return answer

no_rocks = 0

for i in f:
    numbers = list(map(int, i.split()))
    for j in numbers:
        no_rocks += get_length(j, 0, 75)

print(no_rocks)

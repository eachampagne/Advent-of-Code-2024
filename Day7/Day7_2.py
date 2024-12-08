#Advent of Code 2024 Day 7 Part 2
#Solved Dec. 7, 2024

#f = open("sample.txt")
f = open("input.txt")

def find_possibilities(terms):
    possible = [terms[0]]
    operators = [0, 1, 2] #0: add, 1: multiply, 2: concatenate
    #I have a feeling part 2 will be adding more operators...
    #CALLED IT
    #this is so easy to add
    for i in range(1, len(terms)): #iterate over every term in the equation (except the first, which is already addressed)
        new_possible = []
        for j in possible: #iterate over every possible value up to this point in the equation
            for k in operators: #iterate over every possible operator that could go in this space
                match k:
                    case 0:
                        new_result = j + terms[i]
                    case 1:
                        new_result = j * terms[i]
                    case 2:
                        new_result = int(str(j) + str(terms[i]))
                new_possible.append(new_result)
        possible = new_possible
    return possible

answer = 0

for i in f:
    equation = i.split()
    test_value = int((equation[0])[:-1]) #this is dense, but I thought multiple variables would be more confusing
    #basically, the result we're checking against is the first number of the line, dropping the colon, converted to int
    terms = list(map(int, equation[1:])) #and the terms of the equation is every other number in the line, converted to int
    
    possible = find_possibilities(terms)
    if test_value in possible:
        answer += test_value

print(answer)

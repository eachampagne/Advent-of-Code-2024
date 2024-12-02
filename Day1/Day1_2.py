#Advent of Code 2024 Day 1 Part 2
#Solved Dec. 1, 2024

#f = open("sample.txt")
f = open("input.txt")

left_counts = {}
right_counts = {}

#iterate through input file
for i in f:
    numbers = i.split()
    left = int(numbers[0])
    right = int(numbers[1])

    #running total of how many times each number appears in the left list
    if left not in left_counts:
        left_counts[left] = 1
    else:
        left_counts[left] += 1

    #running total of how many times each number appears in the right list 
    if right not in right_counts:
        right_counts[right] = 1
    else:
        right_counts[right] += 1

#Find similarity score
similarity = 0
for i in left_counts.keys():
    if i in right_counts:
        similarity += i * left_counts[i] * right_counts[i] #accounts for a number showing up multiple times in the left list
        #it's symmetric - going through the right list and counting how many times each number appears in the left gives the same answer

print(similarity)

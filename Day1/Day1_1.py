#Advent of Code 2024 Day 1 Part 1
#Solved Dec. 1, 2024

#f = open("sample.txt")
f = open("input.txt")

left_list = []
right_list = []

#iterate through input file
for i in f:
    numbers = i.split()
    left = int(numbers[0])
    right = int(numbers[1])
    
    #insert into lists in proper place: left list
    if len(left_list) == 0: #edge case: nothing in list yet
        left_list.append(left)
    elif left >= left_list[-1]: #edge case: new entry goes at end
        left_list.append(left) #this is the same as the previous branch, but if the list is empty, list[-1] will be out of bounds
    elif left <= left_list[0]: #edge case: entry goes at beginning
        left_list.insert(0, left)
    else:
        unsorted = True
        lower_bound = 0
        upper_bound = len(left_list)
        while unsorted:
            insert_index = int((lower_bound + upper_bound) / 2)
            if left <= left_list[insert_index] and left >= left_list[insert_index - 1]:
                left_list.insert(insert_index, left)
                unsorted = False
            elif left > left_list[insert_index]:
                lower_bound = insert_index
            else: #i.e. left < left_list[insert_index]
                upper_bound = insert_index

    #insert into lists in proper place: right list
    if len(right_list) == 0: #edge case: nothing in list yet
        right_list.append(right)
    elif right >= right_list[-1]: #edge case: new entry goes at end
        right_list.append(right) #this is the same as the previous branch, but if the list is empty, list[-1] will be out of bounds
    elif right <= right_list[0]: #edge case: entry goes at beginning
        right_list.insert(0, right)
    else:
        unsorted = True
        lower_bound = 0
        upper_bound = len(right_list)
        while unsorted:
            insert_index = int((lower_bound + upper_bound) / 2)
            if right <= right_list[insert_index] and right >= right_list[insert_index - 1]:
                right_list.insert(insert_index, right)
                unsorted = False
            elif right > right_list[insert_index]:
                lower_bound = insert_index
            else: #i.e. right < right_list[insert_index]
                upper_bound = insert_index

distance_sum = 0

#iterate through lists to get distances
for left, right in zip(left_list, right_list):
    distance = abs(left - right)
    distance_sum += distance

print(distance_sum)

#Advent of Code 2024 Day 23 Part 2
#Solved Dec. 23, 2024

#An extraordinarily slow code that does in fact work, it just takes ages
#I look forward to seeing other people's more efficient ideas

#find_interlinked_set function now passes it's current connections set to the next iteration rather than building from scratch every time. This makes the code run *much* faster. It's still not fast per se, but less slow.

#f = open("sample.txt")
f = open("input.txt")

connections = {}

size_largest_set = 0
largest_set = set()

#recursively builds list of interconnected computers
#if a group of mutually linked computers are all connected to a single other computer, than the set of the existing set plus the other computer must be a mutually interconnected group as well
def find_interlinked_set(new_set, common_connections):
    global size_largest_set
    global largest_set
    if len(new_set) > size_largest_set:
        size_largest_set = len(new_set)
        largest_set = new_set.copy()
    for i in common_connections:
        follow_up_set = new_set.copy()
        follow_up_set.add(i)
        existing_connections = common_connections.copy()
        existing_connections &= connections[i]
        find_interlinked_set(follow_up_set, existing_connections)

for i in f:
    #parse file
    computers = i.strip().split("-")
    computer_1 = computers[0]
    computer_2 = computers[1]

    #add new connected pair to sets of connected computers
    set_1 = connections.get(computer_1, set())
    set_1.add(computer_2)
    connections[computer_1] = set_1
    set_2 = connections.get(computer_2, set())
    set_2.add(computer_1)
    connections[computer_2] = set_2

    #check if this new pair completes a triangle
    common_connections = set_1 & set_2
    for j in common_connections:
        new_triangle = {computer_1, computer_2, j}
        existing_connections = common_connections.copy()
        existing_connections &= connections[j]
        find_interlinked_set(new_triangle, existing_connections) #if so, check for bigger groupings

lan_list = list(largest_set)
lan_list.sort()

password = lan_list[0]

for i in range(1, len(lan_list)):
    password += ","
    password += lan_list[i]

print(password)

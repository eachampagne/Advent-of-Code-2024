#Advent of Code 2024 Day 23 Part 1
#Solved Dec. 23, 2024

#f = open("sample.txt")
f = open("input.txt")

connections = {}

no_sets_with_ts = 0

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
    if len(common_connections) != 0:
        if computer_1[0] == "t" or computer_2[0] == "t": #if one computer in the new pair starts with t, then every triangle contains a computer that starts with t
            no_sets_with_ts += len(common_connections)
        else: #otherwise only triangles with a previously existing t computer count
            for j in common_connections:
                if j[0] == "t":
                    no_sets_with_ts += 1

print(no_sets_with_ts)

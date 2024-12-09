#Advent of Code 2024 Day 9 Part 1
#Solved Dec. 9, 2024

#I have a feeling part 2 will be to move files without splitting them, just because it's bothering me that you can end up breaking a single file into pieces

#f = open("minisample.txt")
#f = open("sample.txt")
f = open("input.txt")

#free_spaces = {} #dictionary of form index: length
#memory = {} #dictionary of form index: (length, file_id)

free_spaces = [] #list of form (index, length)
memory = [] #list of form (index, length, file_id)

index = 0
file_id = 0
is_file = False #as opposed to free space

for i in f:
    for j in i.strip():
        is_file = not is_file #toggle whether dealing with a file or free space
        chunk_length = int(j)
        if is_file:
            #memory[index] = (chunk_length, file_id)
            memory.append((index, chunk_length, file_id))
            file_id += 1
        else:
            #free_spaces[index] = chunk_length
            free_spaces.append((index, chunk_length))
        index += chunk_length

free_spaces.append((index, 0)) #add an extra 0-length empty space to become the trailing empty space

while len(free_spaces) > 1:
    free_size = free_spaces[0][1]
    data_length = memory[-1][1]

    #if a block can fit in the next empty space, move the whole thing
    if data_length <= free_size:
        data_to_move = memory.pop()
        new_index = free_spaces[0][0]
        moved_data_packet = (new_index, data_to_move[1], data_to_move[2])
        for i in range(len(memory) + 1):
            if i == len(memory):
                memory.append(moved_data_packet)
            elif memory[i][0] > new_index: #this isn't an efficient insertion sort. If I need to optimize, here's something to fix
                memory.insert(i, moved_data_packet)
                break
        #adjust free space accordinging - either the first free space is smaller, or it disappears completely
        if data_length == free_size:
            free_spaces.pop(0)
        else:
            free_spaces[0] = (free_spaces[0][0] + data_length, free_spaces[0][1] - data_length)
        #adjust trailing empty space. If it is now contiguous with a space, merge them
        free_spaces[-1] = (free_spaces[-1][0] - data_length, free_spaces[-1][1] + data_length)
        if len(free_spaces) > 1:
            if free_spaces[-2][0] + free_spaces[-2][1]  == free_spaces[-1][0]:
                free_spaces[-2] = (free_spaces[-2][0], free_spaces[-2][1] + free_spaces[-1][1])
                free_spaces.pop(-1)
    #if the space is too small, move what you can. That space disappears. Keep moving the data block on the next step
    else:
        new_index = free_spaces[0][0]
        free_spaces.pop(0)
        moved_data_packet = (new_index, free_size, memory[-1][2])
        for i in range(len(memory)):
            if memory[i][0] > new_index: #another inefficient sort
                memory.insert(i, moved_data_packet)
                break
        memory[-1] = (memory[-1][0], memory[-1][1] - free_size, memory[-1][2])
        free_spaces[-1] = (free_spaces[-1][0] - free_size, free_spaces[-1][1] + free_size) #trailing free space can't meet another free space because we didn't transfer the whole packet

checksum = 0

for i in memory:
    start_index = i[0]
    length = i[1]
    file_id = i[2]
    checksum += file_id * ((start_index * length) + int(length * (length - 1) / 2))
    #basically since the index of each block within a chunk increases by 1, you can get the sum of indices by modelling as a square - the constant contribution of the starting index - plus a triangle - the increasing contribution of each block
    #this is related to the fact that  integral(x) = 1/2 x^2 + C

print(checksum)

#Advent of Code 2024 Day 9 Part 2
#Solved Dec. 9, 2024

#I have a feeling part 2 will be to move files without splitting them, just because it's bothering me that you can end up breaking a single file into pieces
#...yeah

#f = open("minisample.txt") 
#f = open("sample.txt")
f = open("input.txt")

free_spaces = [] #list of form (index, length)
#memory = [] #list of form (index, length, file_id)
files = {} #dictionary of form file_id: (index, length)
#now going by file id, instead of which is last in memory, so a dictionary is better
#don't want to have to iterate over the whole memory list to find a file
#this requires a small tweak to the final checksum calculation, but the checksum doesn't actually have to be calculated in order...

index = 0
file_id = 0
is_file = False #as opposed to free space

for i in f:
    for j in i.strip():
        is_file = not is_file #toggle whether dealing with a file or free space
        chunk_length = int(j)
        if is_file:
            #memory.append((index, chunk_length, file_id))
            files[file_id] = (index, chunk_length)
            file_id += 1
        else:
            free_spaces.append((index, chunk_length))
        index += chunk_length

max_id = file_id - 1

for file_id in range(max_id, -1, -1):
    to_move = files[file_id]
    current_index = to_move[0]
    data_length = to_move[1]
    for i in range(len(free_spaces)):
        target_index = free_spaces[i][0]
        if target_index >= current_index:
            break
        else:
            free_size = free_spaces[i][1]
            if data_length > free_size:
                continue
            else:
                files[file_id] = (target_index, data_length)
                if data_length == free_size:
                   free_spaces.pop(i)
                else:
                    free_spaces[i] = (free_spaces[i][0] + data_length, free_spaces[i][1] - data_length)
                break
        #don't have to deal with the trailing empty space because no file can get moved into it

checksum = 0

#you don't have to  calculate this in index order
for i in files.keys():
    start_index = files[i][0]
    length = files[i][1]
    file_id = i
    checksum += file_id * ((start_index * length) + int(length * (length - 1) / 2))
    #basically since the index of each block within a chunk increases by 1, you can get the sum of indices by modelling as a square - the constant contribution of the starting index - plus a triangle - the increasing contribution of each block
    #this is related to the fact that integral(x) = 1/2 x^2 + C

print(checksum)

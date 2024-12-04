#Advent of Code 2024 Day 4 Part 1
#Solved Dec. 4, 2024

#f = open("sample.txt")
f = open("input.txt")

grid = []

for i in f:
    grid.append(i.strip())

height = len(grid)
width = len(grid[0]) #this assumes the grid is square...

count = 0
search_text = "XMAS"

#iterate over the grid looking for X's to start searching at
for i in range(len(grid)): #i is row number
    for j in range(len(grid[i])): #j is column number
        if grid[i][j] == search_text[0]: #i.e., == "X"
            for m in range(-1, 2): #define 8 directions originating from a given point
                for n in range(-1, 2):
                    if m != 0 or n != 0: #exclude the zero vector; staying in the same place is bad
                        matches_text = True
                        for k in range(1, len(search_text)): #check each successive letter in the search term
                            #k starts at 1 because we only start searching when we find the 1st letter in the grid somewhere
                            delX = m * k #calculate the offset from the first 
                            delY = n * k
                            x = j + delX
                            y = i + delY
                            #make sure it's in bounds
                            if (x >= 0 and x <= width - 1) and (y >= 0 and y <= height - 1):
                                if grid[y][x] != search_text[k]: #wrong letter - not a match
                                    matches_text = False 
                                    break
                            else: #out of bounds - not a match
                                matches_text = False
                                break
                        if matches_text:
                            count += 1

print(count)

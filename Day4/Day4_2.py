#Advent of Code 2024 Day 4 Part 2
#Solved Dec. 4, 2024

#f = open("sample.txt")
f = open("input.txt")

grid = []

for i in f:
    grid.append(i.strip())

height = len(grid)
width = len(grid[0]) #this assumes the grid is square...

count = 0

#I think it has to be X shaped, not plus shaped
#All of the examples were but the instructions didn't specifically say plus shapes didn't count

#iterate over the grid looking for X's to start searching at
#The edges can't possible be the center of an X, so no point in checking them
#this also guarantees that the neighboring letters are all in bounds, so we don't have to test for that
for i in range(1, len(grid) - 1): #i is row number
    for j in range(1, len(grid[i]) - 1): #j is column number
        if grid[i][j] == "A":
            #it feels like there must be a better way to code this logic, but there really aren't that many possibilities so I guess this will do
            if(
                ( #check diagonal top-left to botton-right - two possibilities
                    (grid[i+1][j+1] == "M" and grid[i-1][j-1] == "S")
                    or
                    (grid[i+1][j+1] == "S" and grid[i-1][j-1] == "M")
                )
                and
                ( #check diagonal bottom-left to top-right - two possibilities
                    (grid[i+1][j-1] == "M" and grid[i-1][j+1] == "S")
                    or
                    (grid[i+1][j-1] == "S" and grid[i-1][j+1] == "M") 
                )
                    ):
                count += 1
print(count)

#Advent of Code 2024 Day 25
#Solved Dec. 25, 2024

#f = open("sample.txt")
f = open("input.txt")

data = f.read()

schematics = data.strip().split("\n\n") #strip to remove trailing \n

no_tumblers = 5
available_height = 5 #not counting bottom or top rows that identify key vs. lock

keys = []
locks = []

for i in schematics:
    is_lock = True if i[0] == "#" else False
    lines = i.split("\n")
    tumblers = []
    for j in range(no_tumblers):
        filled_count = 0
        for k in range(1, len(lines) - 1): #skip first and last line
            if lines[k][j] == "#":
                filled_count += 1
        tumblers.append(filled_count)
    if is_lock:
        locks.append(tuple(tumblers))
    else:
        keys.append(tuple(tumblers))

no_fits = 0

for i in locks:
    for j in keys:
        fits = True
        for k in range(no_tumblers):
            if i[k] + j[k] > available_height:
                fits = False
        if fits:
            no_fits += 1

print(no_fits)

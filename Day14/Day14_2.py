#Advent of Code 2024 Day 14 Part 2
#Solved Dec. 14, 2024

#the answer is 6876 seconds
#this was kind of a pain to solve, since I didn't know what "Christmas tree" meant in terms of position, I couldn't test for it in code and had to check for it manually
#now features a skip function! Can move forward or backwards (relative to your current time - this doesn't skip to a specific time), so don't have to hold down enter while it reaches 6876 seconds
#also now features no longer running forever (or until you Ctrl-C)! Just type "quit". No other command will work though
#I'm not adding a whole command parsing module
#It works, you can validate it without taking forever, and I got the right answer

do_sample = False

if do_sample:
    f = open("sample.txt")
    width = 11
    height = 7
else:
    f = open("input.txt")
    width = 101
    height = 103

no_seconds = 0

positions = []
velocities = []

locations = set()

def display():
    for i in range(height):
        line = ""
        for j in range(width):
            if (j, i) in locations:
                line += "X"
            else:
                line += " "
        print(line)

no_seconds = 0

for i in f:
    data = i.split()
    start_pos = tuple(map(int, data[0].split("=")[1].split(",")))
    velocity = tuple(map(int, data[1].split("=")[1].split(",")))

    positions.append(start_pos)
    velocities.append(velocity)

    locations.add(start_pos)

display()
print(no_seconds)

keep_going = True

while keep_going:
    
    locations = set()

    s = input()

    try:
        seconds = int(s)
    except ValueError:
        if s == "quit":
            keep_going = False
            continue
        seconds = 1

    no_seconds += seconds

    for i in range(len(positions)):
        positions[i] = ((positions[i][0] + seconds * velocities[i][0]) % width, (positions[i][1] + seconds * velocities[i][1]) % height)
        locations.add(positions[i])

    display()
    print(no_seconds)




















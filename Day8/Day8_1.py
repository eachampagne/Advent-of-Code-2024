#Advent of Code 2024 Day 8 Part 1
#Solved Dec. 8, 2024

#f = open("sample.txt")
f = open("input.txt")

#  ----> x
# |
# |
# |
# |
# v y

def is_in_bounds(antinode, width, height):
    return (antinode[0] > 0 and antinode[0] <= width and antinode[1] > 0 and antinode[1] <= width)
           
antennas = {}

y = 0
for i in f:
    y += 1
    x = 0
    for j in i.strip():
        x += 1
        if j != ".":
            antennas[j] = antennas.get(j, []) + [(x, y)]

width = x
height = y

antinodes = set()

for freq in antennas.keys():
    antennas_f = antennas[freq]
    for j in range(len(antennas_f)):
        for k in range(j+1, len(antennas_f)):
            antenna_1 = antennas_f[j]
            antenna_2 = antennas_f[k]
            del_x = antenna_2[0] - antenna_1[0]
            del_y = antenna_2[1] - antenna_1[1]
            antinode_1 = (antenna_1[0] - del_x, antenna_1[1] - del_y)
            antinode_2 = (antenna_2[0] + del_x, antenna_2[1] + del_y)
            if is_in_bounds(antinode_1, width, height):
                antinodes.add(antinode_1)
            if is_in_bounds(antinode_2, width, height):
                antinodes.add(antinode_2)

no_antinodes = len(antinodes)
print(no_antinodes)


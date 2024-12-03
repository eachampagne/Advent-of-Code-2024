#Advent of Code 2024 Day 3 Part 2
#Solved Dec. 3, 2024

import re

#f = open("sample2.txt") #I wasted so much time because I didn't notice that the sample had changed
f = open("input.txt")

sum = 0
enabled = True

mul_regex = re.compile(r"mul\(\d+,\d+\)|do\(\)|don\'t\(\)")

for i in f: #there should only be one i since I think both inputs are a single line - nvm, the input is several lines so it's a good thing I did this
    matches = mul_regex.findall(i)
    for j in matches:
        if j == "do()":
            enabled = True
        elif j == "don\'t()":
            enabled = False
        elif enabled:
            #j must be of form mul(***,***)
            #so the number part is j[4:-1]
            numbers = j[4:-1].split(",") #takes "number part" and splits on the comma - returns a list of two strings
            sum += int(numbers[0]) * int(numbers[1]) #cast those strings to int, multiply, and sum

print(sum)

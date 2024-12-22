#Advent of Code 2024 Day 22 Part 1
#Solved Dec. 22, 2024

#This is going to be the type of problem where you have to figure out how to do it more efficiently
#Need to figure out if I can skip steps somehow. Modulos maybe?
#Or maybe part 1 will just work and I'll only have to optimize for part 2. I'll see how it goes I guess
#So it turns out I am 100% wrong
#Glad I didn't spend time optimizing this function for nothing
#It could probably be faster but it works

#f = open("sample.txt")
f = open("input.txt")

def gen_secret_number(number):
    step_1 = (number ^ (number * 64)) % 16777216
    step_2 = (int(step_1 / 32) ^ step_1) % 16777216
    step_3 = ((step_2 * 2048) ^ step_2) % 16777216
    return step_3

secret_sum = 0
for i in f:
    secret_number = int(i)
    for j in range(2000):
        secret_number = gen_secret_number(secret_number)
    secret_sum += secret_number

print(secret_sum)

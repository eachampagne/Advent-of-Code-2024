#Advent of Code 2024 Day 22 Part 2
#Solved Dec. 22, 2024

#Some thoughts: does the process for generating secret numbers preference certain final digits? Are some digits impossible?
#Does it have any cycles?
#Do some patterns of price changes never occur?

#Nevermind. It turns out if you just keep track of every pattern you've seen, in total and for a particular buyer, you can calculate the running total of bananas for each pattern as you read through the file.

#This runs in a few seconds. There's probably a more optimal way, but I'm satisfied with this.

#f = open("sample2.txt")
f = open("input.txt")

def gen_secret_number(number):
    step_1 = (number ^ (number * 64)) % 16777216
    step_2 = (int(step_1 / 32) ^ step_1) % 16777216
    step_3 = ((step_2 * 2048) ^ step_2) % 16777216
    return step_3

bananas_per_pattern = {}
max_bananas = 0
for i in f:
    secret_number = int(i)
    old_price = secret_number % 10
    prev_changes = []
    patterns_found = set()
    for j in range(2000):
        new_secret_number = gen_secret_number(secret_number)
        new_price = new_secret_number % 10
        price_change = new_price - old_price
        prev_changes.append(price_change)
        if len(prev_changes) > 4:
            prev_changes.pop(0)
        if len(prev_changes) == 4:
            search_pattern = tuple(prev_changes)
            if search_pattern not in patterns_found:
                patterns_found.add(search_pattern)
                bananas_per_pattern[search_pattern] = bananas_per_pattern.get(search_pattern, 0) + new_price
                if bananas_per_pattern[search_pattern] > max_bananas:
                    max_bananas = bananas_per_pattern[search_pattern]
                    best_pattern = search_pattern
                    #I don't actually have to track the best pattern, since the problem only asks for the maximum bananas, not the actual pattern that produces that quantity
                    #But I was curious
        old_price = new_price
        secret_number = new_secret_number
 
print(max_bananas)
print(best_pattern)

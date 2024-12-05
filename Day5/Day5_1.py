#Advent of Code 2024 Day 5 Part 1
#Solved Dec. 5, 2024

#f = open("sample.txt")
f = open("input.txt")

rules_before = {} #the set of pages that a given page (the key) must go before
rules_after = {} #the set of pages that a given page (the key) must go after
#I'm using sets instead of lists for the data in the dictionary firstly because I only recently learned this is a builtin class, so I want to try it out, and secondly because I think one of the set operations will be helpful

parsing_rules = True
answer = 0

#Iterate through the input file
for i in f:
    if i == "\n":
        parsing_rules = False
        continue
    elif parsing_rules:
        rule = i.split("|")
        before = int(rule[0])
        after = int(rule[1])
        if after in rules_after:
            rules_after[after].add(before)
        else:
            rules_after[after] = {before}
        if before in rules_before:
            rules_before[before].add(after)
        else:
            rules_before[before] = {after}
    else:
        pages = list(map(int, i.split(",")))
        is_ordered = True
        for j in range(len(pages)):
            page_to_check = pages[j]
            pages_before = set(pages[:j])
            pages_after = set(pages[j+1:])
            if len(pages_before & rules_before.get(page_to_check, set())) != 0 or len(pages_after & rules_after.get(page_to_check,set())) != 0:
                is_ordered = False
                break
        if is_ordered:
            middle_page_index = int(len(pages) / 2) #round down to get the target index
            #this assumes every group has an odd number of pages, but it must to define a middle page
            answer += pages[middle_page_index]
        
print(answer)

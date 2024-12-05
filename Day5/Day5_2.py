#Advent of Code 2024 Day 5 Part 2
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
        not_ordered = False
        for j in range(len(pages)): #if already ordered, do nothing with this listing, continue to next entry
            page_to_check = pages[j]
            pages_before = set(pages[:j])
            pages_after = set(pages[j+1:])
            if len(pages_before & rules_before.get(page_to_check, set())) != 0 or len(pages_after & rules_after.get(page_to_check,set())) != 0:
                not_ordered = True
                break
        if not_ordered: #fix out of order lists
            ordered_pages = []
            while len(pages) != 0: #move pages from "to sort" pile (pages) to "sorted" pile (ordered_pages)
                page_to_insert = pages.pop(0)
                is_sorted = False
                if len(ordered_pages) == 0: #edge case - first entry, ordered_pages is empty
                    ordered_pages.append(page_to_insert)
                    is_sorted = True
                elif len(set(ordered_pages) & rules_before.get(page_to_insert,set())) == 0: #edge case - should go at end of sorted list (this if statement prevents array out of bounds errors
                    ordered_pages.append(page_to_insert)
                    is_sorted = True
                else:
                    for j in range(len(ordered_pages)):
                        pages_before = set(ordered_pages[:j])
                        pages_after = set(ordered_pages[j:])
                        if len(pages_before & rules_before.get(page_to_insert, set())) == 0 and len(pages_after & rules_after.get(page_to_insert, set())) == 0:
                            ordered_pages.insert(j, page_to_insert)
                            is_sorted = True
                            break
                if not is_sorted: #it is possible (at least in theory, though maybe not in my input data) that there isn't yet enough information for there to be a unique place to sort a page. In this case, place it at the end of the "to sort" pile and return later
                    #I coded my algorithm wrong and it actually inserts each page at the first slot that doesn't break any rules, even if that's not the only slot, so this code never runs. It happens that with my input file I get the right final answer anyway (I guess I might have pages in the wrong order, but as long as the middle term is right it doesn't matter). However I can think of edge cases that my code would not work for. I tried, in a different script (not included on GitHub), to address these edge cases. In the process I learned that my input has at least one circular loop of rules (a situation where x|y, y|z, and z|x, requiring that noindividual list of pages contains all of x, y, and z). This means the transitive property doesn't hold, so my plan to create a more general algorithm won't work. I can't prove that there is no way, but I'm accepting that everyone's inputs are designed to be solvable, and I solved the actual problem if not the general case, so I'm not going to put any more time into this.
                    #At any rate, I could have just tried every permutation of pages orders until one worked, so even had I completely abandoned my dubious sorting algorithm I could have solved the problem.
                    #Update - according to posts online, that would not have taken a very very long time
                    #Mine works, at least well enough. 
                    pages.insert(page_to_insert)

            middle_page_index = int(len(ordered_pages) / 2) #round down to get the target index
            #this assumes every group has an odd number of pages, but it must to define a middle page
            answer += ordered_pages[middle_page_index]
        
print(answer)

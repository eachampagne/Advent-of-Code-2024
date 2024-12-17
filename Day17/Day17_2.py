#Advent of Code Day 17 Part 2
#Solved Dec. 17, 2024

#I've been trying not to go crazy with classes this AOC, but I think making a class for the computer would actually be helpful here

class Computer3Bit:
    def __init__(self, regA, regB, regC, program, verbose = True):
        self.regA = regA
        self.regB = regB
        self.regC = regC

        self.program = program

        self.verbose = verbose

        self.pointer = 0 #the instruction pointer

        self.hasHalted = False

        self.programLength = len(self.program)

        self.output = ""

    def run(self):
        while not self.hasHalted:
            self.next_instruction()
        return self.output

    def next_instruction(self):
        if self.pointer + 1 >= self.programLength: #need to make certain the operand isn't out of bounds either
            self.hasHalted = True
        else:
            opcode = self.program[self.pointer]
            operand = self.program[self.pointer + 1]
            jump = False
            match opcode:
                case 0:
                    self.adv(operand)
                case 1:
                    self.bxl(operand)
                case 2:
                    self.bst(operand)
                case 3:
                    jump = self.jnz(operand)
                case 4:
                    self.bxc(operand)
                case 5:
                    self.out(operand)
                case 6:
                    self.bdv(operand)
                case 7:
                    self.cdv(operand)
            if not jump:
                self.pointer += 2        

    def adv(self, operand):
        combo_op = self.get_combo_op(operand)
        numerator = self.regA
        denom = 2 ** combo_op
        self.regA = int(numerator / denom)

    def bxl(self, operand):
        self.regB = self.regB ^ operand

    def bst(self, operand):
        combo_op = self.get_combo_op(operand)
        self.regB = combo_op % 8

    def jnz(self, operand):
        if self.regA != 0:
            self.pointer = operand
            return True
        else:
            return False

    def bxc(self, operand):
        self.regB = self.regB ^ self.regC

    def out(self, operand):
        combo_op = self.get_combo_op(operand)
        out = combo_op % 8
        if self.output != "":
            self.output += "," + str(out)
        else:
            self.output = str(out)
        if self.verbose:
            print(out)

    def bdv(self, operand):
        combo_op = self.get_combo_op(operand)
        numerator = self.regA
        denom = 2 ** combo_op
        self.regB = int(numerator / denom)

    def cdv(self, operand):
        combo_op = self.get_combo_op(operand)
        numerator = self.regA
        denom = 2 ** combo_op
        self.regC = int(numerator / denom)

    def get_combo_op(self, operand):
        match operand:
            case _ if operand <= 3:
                return operand
            case 4:
                return self.regA
            case 5:
                return self.regB
            case 6:
                return self.regC
            case 7:
                print("reserved operand!")

    def dump_state(self):
        print("Reg A: " + str(self.regA))
        print("Reg B: " + str(self.regB))
        print("Reg C: " + str(self.regC))
        print("Instruction pointer: " + str(self.pointer))
        print("Program: " + str(self.program))
        print("Halted? " + str(self.hasHalted))

###################

#this needs to be recursive because some branches dead end
def solve_for_target(target_A, remaining_targets):
    if len(remaining_targets) == 0:
        return target_A
    current_target = remaining_targets.pop(0)
    #each new A_reg is int(A/8)
    #So to work backwards from a target A value, the previous A can be A*8 to (A+1) * 8 -1
    #or range(A*8, (A+1)*8)
    for test_A in range(target_A*8, (target_A+1) * 8): #did a bunch of work on paper
        #my program was nice in that there was only one jump instruction, that either returned to the beginning of the program or halted
        #It couldn't jump to the middle, or worse, to an odd-numbered instruction
        #There was only one print statement
        #Both reg_B and reg_C depended on reg_A for every loop through the program, no carrying over
        #Still involved a lot of pencil and paper solving to figure out reg_B and reg_C in terms of reg_A for each iteration
        #I don't know if this problem would even have been solvable without these constraints
        test_B = ((test_A % 8) ^ 1) ^ 5
        test_C = int(test_A / (2**((test_A % 8) ^ 1)))
        value_out = (test_B ^ test_C) % 8
        if value_out == current_target:
            solution = solve_for_target(test_A, remaining_targets.copy()) #If you don't copy, it'll mess up moving up to try different branches
            if solution != -1:
                return solution
    return -1 #no solution found, try a different branch

#1. Parse input file
#f = open("sample2.txt") #this won't work on the sample. The recursive solving function is hand-crafted to match my pen-and-paper work
#Making it dynamically work out the solution from the program would be cool, but much more difficult
#So no general solution today
f = open("input.txt")

lines = f.read().split("\n")

regA = int(lines[0].split()[-1])
regB = int(lines[1].split()[-1])
regC = int(lines[2].split()[-1])

program_string = lines[4].split()[-1]
program = list(map(int, program_string.split(",")))

#2. Solve

#need to work backwards, so reverse this list
#I guess I could have popped off the back, oh well
#I needed to copy it regardless to use it in the computer to check my answer
target_values = list(reversed(program))

target_A = 0 #need last A to be 0 for program to halt

solution = solve_for_target(target_A, target_values)

print(solution)

#3. Run the simulation to test solution
#Not strictly necessary, but it would be a shame not to use my nice computer class!
computer = Computer3Bit(solution, regB, regC, program, False)
computer_output = computer.run()

if computer_output == program_string:
    print("solution works!")    

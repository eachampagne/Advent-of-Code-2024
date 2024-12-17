#Advent of Code Day 17 Part 1
#Solved Dec. 17, 2024

#I've been trying not to go crazy with classes this AOC, but I think making a class for the computer would actually be helpful here

class Computer3Bit:
    def __init__(self, regA, regB, regC, program):
        self.regA = regA
        self.regB = regB
        self.regC = regC

        self.program = program

        self.pointer = 0 #the instruction pointer

        self.hasHalted = False

        self.programLength = len(self.program)

        self.output = ""

    def run(self):
        while not self.hasHalted:
            self.next_instruction()

    def next_instruction(self):
        if self.pointer + 1 >= self.programLength: #need to make certain the operand isn't out of bounds either
            self.hasHalted = True
            print(self.output)
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

#f = open("sample.txt")
f = open("input.txt")

lines = f.read().split("\n")

regA = int(lines[0].split()[-1])
regB = int(lines[1].split()[-1])
regC = int(lines[2].split()[-1])

program = list(map(int, lines[4].split()[-1].split(",")))

computer = Computer3Bit(regA, regB, regC, program)

computer.run()

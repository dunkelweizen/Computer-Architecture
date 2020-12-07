"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0

    def ram_read(self, MAR):
        return self.ram[MAR]

    def ram_write(self, MAR, MDR):
        self.ram[MAR] = MDR

    def load(self, file):
        """Load a program into memory."""

        address = 0

        file = open(file, 'r')
        program = file.readlines()

        for instruction in program:
            if instruction[0] != "#" and instruction != '\n':
                instruction = instruction[:8]
                self.ram[address] = int(instruction,2)
                address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        while self.pc < len(self.ram):
            ir = self.pc
            instruction = self.ram_read(ir)
            num_operands = instruction >> 6
            if instruction == 0b0001:
                # HLT
                break
            operand_a = None
            operand_b = None
            if num_operands == 2:
                operand_a = self.ram_read(ir+1)
                operand_b = self.ram_read(ir+2)
                self.pc += 3
            if num_operands == 1:
                operand_a = self.ram_read(ir+1)
                self.pc += 2
            if num_operands == 0:
                self.pc += 1
            if instruction == 0b10000010:
                self.LDI(operand_a, operand_b)
            elif instruction == 0b01000111:
                self.PRN(operand_a)
            elif instruction == 0b10100010:
                self.MUL(operand_a,operand_b)


    def LDI(self, address, value):
        self.reg[address] = value

    def PRN(self, address):
        print(self.reg[address])

    def MUL(self, address1, address2):
        self.reg[address1] = self.reg[address1] * self.reg[address2]
"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.fl = 0
        self.sp = 7
        self.ef = 0
        self.ltf = 0
        self.gtf = 0

    def ram_read(self, mar):
        return self.ram[mar]

    def ram_write(self, mdr, mar):
        self.ram[mar] = mdr
        return self.ram[mar]

    def load(self, filename):
        """Load a program into memory."""
        try:
            address = 0
            with open(filename) as f:
                for line in f:
                    line = line.split('#', 1)[0]
                    value = line.rstrip()
                    if value == "":
                        continue
                    num = int(value, 2)
                    # print(num)
                    self.ram_write(num, address)
                    address += 1
        except FileNotFoundError:
            print("File not found")
            sys.exit(2)

        # program = [
        #     # From print8.ls8
        #     0b10000010,  # LDI R0,8     | - 3 slots
        #     0b00000000,  # | -
        #     0b00001000,  # | -
        #     0b01000111,  # PRN R0       | - 2 slots
        #     0b00000000,  # | -
        #     0b00000001,  # HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        running = True
        # Set flag register
        self.reg[self.fl] = 0
        # Instructions Decoded from LS8-spec
        LDI = 0b10000010
        PRN = 0b01000111
        HLT = 0b00000001
        MUL = 0b10100010
        PUS = 0b01000101
        POP = 0b01000110
        CAL = 0b01010000
        RET = 0b00010001
        ADD = 0b10100000

        CMP = 0b10100111
        JMP = 0b01010100
        JEQ = 0b01010101
        JNE = 0b01010110

        while True:
            # This is the Instruction Register as 'command'
            command = self.ram_read(self.pc)
            #  op_a needs to read next byte after PC
            operand_a = self.ram_read(self.pc + 1)
            #  op_b needs to read next 2 bytes after PC
            operand_b = self.ram_read(self.pc + 2)
            # print('Running ---', IR)

            if command == JNE:
                # If `E` flag is clear (false, 0), jump to the address stored in the given
                # register.
                if self.ef is 0:
                    reg = self.ram[self.pc + 1]
                    self.pc = self.reg[reg]
                    print("JNE activated")
                else:
                    self.pc += 2
                    print("JNE not activated")

            if command == JEQ:
                # If `equal` flag is set (true), jump to the address stored in the given register.
                if self.ef is not 0:
                    reg = self.ram[self.pc + 1]
                    self.pc = self.reg[reg]
                    print("JEQ activated")
                else:
                    self.pc += 2
                    print("JEQ not activated")
                    # sys.exit(0)

            if command == CMP:
                # Compare the values in two registers.
                reg_a = self.reg[operand_a]
                reg_b = self.reg[operand_b]
                # * If they are equal, set the Equal `E` flag to 1, otherwise set it to 0.
                if reg_a == reg_b:
                    self.ef = 1
                    self.pc += 1
                    print('ef + 1')
                else:
                    # self.ef = 0
                    self.pc += 1
                # * If registerA is less than registerB, set the Less-than `L` flag to 1,
                # otherwise set it to 0.
                if reg_a < reg_b:
                    self.ltf = 1
                    self.pc += 1
                    print('ltf + 1')
                else:
                    self.ltf = 0
                    self.pc += 1
                # # * If registerA is greater than registerB, set the Greater-than `G` flag
                # # to 1, otherwise set it to 0.
                # if reg_a > reg_b:
                #     self.gtf = 1
                #     self.pc += 1
                #     print('gtf + 1')
                # else:
                #     self.gtf = 0
                #     self.pc += 1

                self.pc += 1

            if command == JMP:
                # Jump to the address stored in the given register.
                reg = self.ram[self.pc + 1]

                # Set the `PC` to the address stored in the given register.
                self.pc = self.reg[reg]

            if command == CAL:
                # Calls a subroutine (function) at the address stored in the register.

                # 1. The address of the instruction directly after `CALL` is
                #    pushed onto the stack.
                self.reg[self.sp] -= 1
                self.ram[self.reg[self.sp]] = self.pc + 2
                #    This allows us to return to where we left off when the
                #    subroutine finishes executing.

                # 2. The PC is set to the address stored in the given register.
                reg = self.ram[self.pc + 1]
                self.pc = self.reg[reg]
                #    We jump to that location in RAM and execute the first instruction
                #    in the subroutine.
                #    The PC can move forward or backwards from its current location.

            if command == RET:
                # Return from subroutine
                # Pop the value from the top of the stack and store it in the `PC`.
                self.pc = self.ram[self.reg[self.sp]]
                self.reg[self.sp] += 1

            if command == ADD:
                reg_a = self.ram[self.pc + 1]
                reg_b = self.ram[self.pc + 2]
                self.reg[reg_a] += self.reg[reg_b]
                self.pc += 3

            if command == PUS:
                # Grab the register argument
                reg = self.ram[self.pc + 1]
                val = self.reg[reg]
                # Decrement the SP
                self.reg[self.sp] -= 1
                # Copy the value in the given register to the address pointed to by SP.
                self.ram[self.reg[self.sp]] = val
                self.pc += 2
                print("PUSH")

            if command == POP:
                # Grab the value from the top of the stack
                reg = self.ram[self.pc + 1]
                val = self.ram[self.reg[self.sp]]
                # Decrement the SP
                self.reg[reg] = val
                # Increment SP
                self.reg[self.sp] += 1
                self.pc += 2
                print("POP")

            if command == HLT:
                print("HALT")
                running = False
                sys.exit(0)

            if command == MUL:
                # Multiply the values in two registers together and store in reg A
                multi = self.reg[operand_a] * self.reg[operand_b]
                self.reg[operand_a] = multi
                self.pc += 3
                print("MUL")

            if command == LDI:
                # Set the value of a register to an integer
                # Now put value in correct register
                self.reg[operand_a] = operand_b
                print("Register:", self.reg)
                # used both, so advance by 3 to start at next correct value
                # op_a will be 1 ahead from current pos, op_b 2
                print("PC", self.pc)
                # self.trace()
                self.pc += 3

            if command == PRN:
                # PRN: register pseudo-instruction
                # print numeric value stored in given register
                print()
                print(f"***PRINTING***", self.reg[operand_a])
                print()
                # self.trace()
                print("Register:", self.reg)
                print("PC", self.pc)
                self.pc += 2

            # else:
            #     # self.trace()
            #     print("------------------")
            #     print("IR, 130 = LDI =>", command)
            #     print("PC", self.pc)
            #     print("reg", self.reg)
            #     print("Equal", self.ef)
            #     print("op_a", operand_a)
            #     print("op_b", operand_b)
            #     print("------------------")

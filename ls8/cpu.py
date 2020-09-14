"""CPU functionality."""
import sys
# opcodes
LDI = 0b10000010
PRN = 0b01000111
HLT = 0b00000001
JEQ = 0b01010101
JNE = 0b01010110
JMP = 0b01010100
# Alu opcodes
CMP = 0b10100111
AND = 0b10101000
OR =  0b10101010
XOR = 0b10101011
NOT = 0b01101001
SHL = 0b10101100
SHR = 0b10101101
MOD = 0b10100100

class CPU:
    """Main CPU class."""
    def __init__(self):
        """Construct a new CPU."""
        # Total memory
        self.ram = [0] * 256
        # General register
        self.reg = [0] * 8
        # Program Counter
        self.PC = 0
        # Store the starting position of stack pointer in register 7.
        self.reg[7] = 0xF4
        # Flag 
        self.FL = 0b00000000
        self.running = False
        self.instruction_mapping = dict()
        self.instruction_mapping[LDI] = self._ldi
        self.instruction_mapping[PRN] = self._prn
        self.instruction_mapping[HLT] = self._hlt
        self.instruction_mapping[JEQ] = self._jeq
        self.instruction_mapping[JNE] = self._jne
        self.instruction_mapping[JMP] = self._jmp
        # ALU oprations
        self.instruction_mapping[CMP] = self._cmp
        self.instruction_mapping[AND] = self._and
        self.instruction_mapping[OR] = self._or
        self.instruction_mapping[XOR] = self._xor
        self.instruction_mapping[NOT] = self._not
        self.instruction_mapping[SHL] = self._shl
        self.instruction_mapping[SHR] = self._shr
        self.instruction_mapping[MOD] = self._mod     
    def load(self, filename):
        """Load a program into memory."""
        address = 0
        # Open file and load in memory
        with open(filename) as file:
            for line in file:
                split_line = line.split("#")
                instruction = split_line[0].strip()
                if instruction != '':
                    self.ram[address] =  int(instruction, 2)
                    address += 1

            
    def ram_read(self, mar):
        return self.ram[mar]
    def ram_write(self, mar, mdr):
        self.ram[mar] = mdr
    # Set value in register
    def _ldi(self, *params):
        self.reg[params[0]] = params[1]
        # Move pointer to next instruction
        self.PC += 3
    # Print value from register
    def _prn(self, *params):
        print(self.reg[params[0]])
        self.PC += 2
    # Compare two register values
    def _cmp(self, *params):
        self.alu("CMP", *params)
        self.PC += 3
    # Jump pc equal flag is 1.
    def _jeq(self, *param):
        if self.FL == 1:
            # Set pc at the given register value
            self.PC = self.reg[param[0]]
        else:
            self.PC += 2
    # Jump pc not equal flag is 1.
    def _jne(self, *param):
        if self.FL != 1:
            # Set pc at the given register value
            self.PC = self.reg[param[0]]
        else:
            self.PC += 2
    # Jump pc at the give register value
    def _jmp(self, *param): 
        self.PC = self.reg[param[0]]
    # AND registerA registerB
    def _and(self, *params):
        self.alu("AND", *params)
     # OR registerA registerB
    def _or(self, *params):
        self.alu("OR", *params)
    # XOR registerA registerB
    def _xor(self, *params):
        self.alu("XOR", *params)
    # NOT register
    def _not(self, *params):
        self.alu("NOT", *params)
    # Shift the value in registerA left by the number of bits specified in registerB.
    def _shl(self, *params):
        self.alu("SHL", *params)
    # Shift the value in registerA right by the number of bits specified in registerB.
    def _shr(self, *params):
        self.alu("SHR", *params)
    # MOD registerA registerB
    def _mod(self, *params):
        self.alu("MOD", *params)
    # Exit from program
    def _hlt(self, *params):
        self.running = False
        exit(1)
    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        if op == "CMP":
            if self.reg[reg_a] < self.reg[reg_b]:
                self.FL = 0b00000100
            elif self.reg[reg_a] > self.reg[reg_b]:
                self.FL = 0b00000010
            else:
                self.FL = 0b00000001
        elif op == "AND":
            self.reg[reg_a] &= self.reg[reg_b]
        elif op == "OR":
            self.reg[reg_a] |= self.reg[reg_b]
        elif op == "XOR":
            self.reg[reg_a] ^= self.reg[reg_b]
        elif op == "NOT":
            self.reg[reg_a] = ~self.reg[reg_a] 
        elif op == "SHL":
            self.reg[reg_a] <<= self.reg[reg_b] 
        elif op == "SHR":
            self.reg[reg_a] >>= self.reg[reg_b]
        elif op == "MOD":
            self.reg[reg_a] %= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")
    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """
        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.PC,
            #self.fl,
            #self.ie,
            self.ram_read(self.PC),
            self.ram_read(self.PC + 1),
            self.ram_read(self.PC + 2)
        ), end='')
        for i in range(8):
            print(" %02X" % self.reg[i], end='')
        print()
    def run(self):
        """Run the CPU."""
        self.running = True
        while self.running:
            # get current instruction and store in memory
            instruction = self.ram_read(self.PC)
            # store bytes
            operand_a = self.ram_read(self.PC + 1)
            operand_b = self.ram_read(self.PC + 2)
            if instruction in self.instruction_mapping:
                self.instruction_mapping[instruction](operand_a, operand_b)
            else:
                print(f"Unknown Instruction {instruction} {bin(instruction)}")
                exit(1)
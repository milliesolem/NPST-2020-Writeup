RECURSION_LIMIT = 1000

from functools import reduce
import struct

"""
"DataView"-klassen var noe jeg fant på nettet, siden python ikke støttet det men det ble brukt i runtime.ts
"""

class DataView:
    def __init__(self, array, bytes_per_element=1):
        self.array = array
        self.bytes_per_element = 1

    def __get_binary(self, start_index, byte_count, signed=False):
        integers = [self.array[start_index + x] for x in range(byte_count)]
        bytes = [integer.to_bytes(self.bytes_per_element, byteorder='little', signed=signed) for integer in integers]
        return reduce(lambda a, b: a + b, bytes)

    def get_uint_16(self, start_index):
        bytes_to_read = 2
        return int.from_bytes(self.__get_binary(start_index, bytes_to_read), byteorder='little')

"""
Følgende er for det meste runtime.ts portet til python, med liten modifikasjon til XOR-operasjoner
"""

def readInstruction(memorySlice):
	instruction = DataView(memorySlice).get_uint_16(0)
	return {
		"operationClass": instruction & 0xf,
		"operation": (instruction >> 4) & 0xf,
		"address": instruction >> 4,
		"value": instruction >> 8,
		"argument1": (instruction >> 8) & 0xf,
		"argument2": (instruction >> 12) & 0xf,
	}

def load(executable):
	if len(executable)>4096:
		raise Exception("Programmet får ikke plass i minnet")

	magic = executable[0:7].decode()
	if magic != ".SLEDE8":
		raise Exception("Dette skjønner jeg ingenting av")

	memory = [0] * 4096
	seek = 7
	i = 0
	while seek < len(executable):
		memory[i] = executable[seek]
		i += 1
		seek += 1
	return memory


def step(exectuable, stdin, maxTicks = 100000):
	inputPtr = 0
	tick = 0

	pc = 0
	flag = False
	regs = [0] * 16
	memory = load(exectuable)
	stdout = []
	backtrace = []

	while pc < len(memory):
		tick += 1
		if tick > maxTicks:
			raise Exception(f"Programmet ble brutalt drept etter å ha benyttet hele {maxTicks} sykluser")
		yield [pc, flag, regs, memory, stdout, inputPtr]
		instr = readInstruction(memory[pc:pc+2])
		pc += 2;

		# HALT
		if instr["operationClass"] == 0x0:
			break
		# SET
		elif instr["operationClass"] == 0x1:
			regs[instr["operation"]] = instr["value"]
		elif instr["operationClass"] == 0x2:
			regs[instr["operation"]] = regs[instr["argument1"]]

		 # FINN
		elif instr["operationClass"] == 0x3:
			regs[1] = (instr["address"] & 0x0f00) >> 8
			regs[0] = instr["address"] & 0xff


		# LOAD / STORE
		elif instr["operationClass"] == 0x4:
			addr = ((regs[1] << 8) | regs[0]) & 0xfff
			if instr["operation"] == 0: regs[instr["argument1"]] = memory[addr]
			elif instr["operation"] == 1: memory[addr] = regs[instr["argument1"]];
			else: raise Exception("Segmenteringsfeil")
		# ALU
		elif instr["operationClass"] == 0x5:
			reg1 = regs[instr["argument1"]]
			reg2 = regs[instr["argument2"]]


			if instr["operation"] == 0x0: regs[instr["argument1"]] &= reg2

			elif instr["operation"] == 0x1: regs[instr["argument1"]] |= reg2
			elif instr["operation"] == 0x2:
				regs[instr["argument1"]] ^= reg2
				# legger til resultat av XOR-operasjon
				xored.append(regs[instr["argument1"]])
			elif instr["operation"] == 0x3:
				regs[instr["argument1"]] = (reg1 << reg2) & 0xff
			elif instr["operation"] == 0x4: regs[instr["argument1"]] >>= reg2
			elif instr["operation"] == 0x5:
				regs[instr["argument1"]] = (reg1 + reg2) & 0xff
			elif instr["operation"] == 0x6:
				regs[instr["argument1"]] = (reg1 - reg2) & 0xff
			else: raise Exception("Segmenteringsfeil")

		# I/O
		elif instr["operationClass"] == 0x6:

			# READ
			if instr["operation"] == 0x0:
				if len(stdin) > inputPtr:
					regs[instr["argument1"]] = stdin[inputPtr]
					inputPtr += 1
				else:
					raise Exception("Programmet gikk tom for føde")

			# WRITE
			elif instr["operation"] == 0x1:
				stdout.append(regs[instr["argument1"]])
				#print(chr(regs[instr["argument1"]]), end="")
			else:
				raise Exception("Segmenteringsfeil")
		# CMP
		elif instr["operationClass"] == 0x7:
			reg1 = regs[instr["argument1"]]
			reg2 = regs[instr["argument2"]]

			if instr["operation"] == 0x0: flag = reg1 == reg2
			elif instr["operation"] == 0x1: flag = reg1 != reg2
			elif instr["operation"] == 0x2: flag = reg1 < reg2
			elif instr["operation"] == 0x3: flag = reg1 <= reg2
			elif instr["operation"] == 0x4: flag = reg1 > reg2
			elif instr["operation"] == 0x5: flag = reg1 >= reg2
			else: raise Exception("Segmenteringsfeil")

		# JMP
		elif instr["operationClass"] == 0x8: pc = instr["address"]
		# COND JMP
		elif (instr["operationClass"] == 0x9):
			if flag:
				pc = instr["address"]
		# CALL
		elif instr["operationClass"] == 0xa:
			if len(backtrace) >= RECURSION_LIMIT:
				raise Exception("Alt for mange funksjonskall inni hverandre")
			backtrace.append(pc)
			pc = instr["address"]

		# RET
		elif instr["operationClass"] == 0xb:
			pc = backtrace.pop(-1) or None
			if pc == None: raise Exception("Segmenteringsfeil")
		elif instr["operationClass"] == 0xc:
			continue
		else:
			raise Exception("Segmenteringsfeil")


"""
Dette er hvor egg klekkes
"""

ex = open("💀.s8","rb").read()
output = []

# mulige tegn i egget
alph = "abcdefghijklmnopqrstuvwxyz"
charset = alph + alph.upper() + "0123456789" + "!:_)+-=[]{}&%#"
# variabel for å gjette egget
crib = "E"
# variabler for å evaluere om vi har gjettet riktig tegn
oldscore = 0
score = 0
# index på tegn i charset som blir gjettet
testChar = 0
while True:
    # sjekker hvis vi har flere nuller i XOR-operasjonene siden sist
    # hvis ja, har vi gjettet riktig tegn
    if score > oldscore:
        crib+=charset[testChar]
        testChar = 0
        print("".join(password)[:len(crib)])
    else:
        testChar += 1
    # hvis vi har klart å gjette oss fram til }, så har vi egget
    if crib[-1]=="}":
        break
    
    xored = []
    password = crib+charset[testChar]+"A" * 40
    for i in step(ex,password.encode()):
        output.append(i)
        
    oldscore = score
    score = 0
    # teller antall nuller i starten av de siste 28 tegnene
    for i in xored[-28:]:
        if i!=0:
            break
        score+=1
















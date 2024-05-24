import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from enum import Enum
import re, shlex
import registers as regs
import address as address

R0, R1, R2, R3, R4, R5, R6, R7, R8, R9, R10, R11, R12, R13, R14, R15, pc, sl, sb, sp, fp, hp = regs.registers.values()
registers = {'R0':R0, 'R1':R1, 'R2':R2, 'R3':R3, 'R4':R4, 'R5':R5, 'R6':R6, 'R7':R7, 'R8':R8, 'R9':R9, 'R10':R10, 'R11':R11, 'R12':R12, 'R13':R13, 'R14':R14, 'R15':R15, 'pc':pc, 'sl':sl, 'sb':sb, 'sp':sp, 'fp':fp, 'hp':hp} 
firstInstruction = [-1]
stackSize = 500
memory = []

class directives(Enum):
    INT = 1
    BYT = 2
    BTS = 3
    STR = 4

class instructions(Enum):
    JMP = 1
    JMR = 2
    BNZ = 3
    BGT = 4
    BLT = 5
    BRZ = 6
    MOV = 7
    MOVI = 8
    LDA = 9
    STR = 10
    LDR = 11
    STB = 12
    LDB = 13
    ISTR = 14
    ILDR = 15
    ISTB = 16
    ILDB = 17
    ADD = 18
    ADDI = 19
    SUB = 20
    SUBI = 21
    MUL = 22
    MULI = 23
    DIV = 24
    SDIV = 25
    DIVI = 26
    AND = 27
    OR = 28
    CMP = 29
    CMPI = 30
    TRP = 31
    ALCI = 32
    ALLC = 33
    IALLC = 34
    PSHR = 35
    PSHB = 36
    POPR = 37
    POPB = 38
    CALL = 39
    RET = 40

    def get(val):
        if type(val) == str:
            match val:
                case 'JMP':
                    return 1
                case 'JMR':
                    return 2
                case 'BNZ':
                    return 3
                case 'BGT':
                    return 4
                case 'BLT':
                    return 5
                case 'BRZ':
                    return 6
                case 'MOV':
                    return 7
                case 'MOVI':
                    return 8
                case 'LDA':
                    return 9
                case 'STR':
                    return 10
                case 'LDR':
                    return 11
                case 'STB':
                    return 12
                case 'LDB':
                    return 13
                case 'ISTR':
                    return 14
                case 'ILDR':
                    return 15
                case 'ISTB':
                    return 16
                case 'ILDB':
                    return 17
                case 'ADD':
                    return 18
                case 'ADDI':
                    return 19
                case 'SUB':
                    return 20
                case 'SUBI':
                    return 21
                case 'MUL':
                    return 22
                case 'MULI':
                    return 23
                case 'DIV':
                    return 24
                case 'SDIV':
                    return 25
                case 'DIVI':
                    return 26
                case 'AND':
                    return 27
                case 'OR':
                    return 28
                case 'CMP':
                    return 29
                case 'CMPI':
                    return 30
                case 'TRP':
                    return 31
                case 'ALCI':
                    return 32
                case 'ALLC':
                    return 33
                case 'IALLC':
                    return 34
                case 'PSHR':
                    return 35
                case 'PSHB':
                    return 36
                case 'POPR':
                    return 37
                case 'POPB':
                    return 38
                case 'CALL':
                    return 39
                case 'RET':
                    return 40
                case _:
                    return 0
        else:
            match val:
                case 1:
                    return 'JMP'
                case 2:
                    return 'JMR'
                case 3:
                    return 'BNZ'
                case 4:
                    return 'BGT'
                case 5:
                    return 'BLT'
                case 6:
                    return 'BRZ'
                case 7:
                    return 'MOV'
                case 8:
                    return 'MOVI'
                case 9:
                    return 'LDA'
                case 10:
                    return 'STR'
                case 11:
                    return 'LDR'
                case 12:
                    return 'STB'
                case 13:
                    return 'LDB'
                case 14:
                    return 'ISTR'
                case 15:
                    return 'ILDR'
                case 16:
                    return 'ISTB'
                case 17:            
                    return 'ILDB'
                case 18:
                    return 'ADD'    
                case 19:
                    return 'ADDI'
                case 20:
                    return 'SUB'
                case 21:
                    return 'SUBI'
                case 22:
                    return 'MUL'
                case 23:
                    return 'MULI'
                case 24:
                    return 'DIV'
                case 25:
                    return 'SDIV'
                case 26:
                    return 'DIVI'
                case 27:
                    return 'AND'
                case 28:
                    return 'OR'
                case 29:
                    return 'CMP'
                case 30:
                    return 'CMPI'
                case 31:
                    return 'TRP'
                case 32:
                    return 'ALCI'
                case 33:
                    return 'ALLC'
                case 34:
                    return 'IALLC'
                case 35:
                    return 'PSHR'
                case 36:
                    return 'PSHB'
                case 37:
                    return 'POPR'    
                case 38:
                    return 'POPB'
                case 39:
                    return 'CALL'
                case 40:
                    return 'RET'
                case _:
                    return 0

def makeBinary(value, bits=32):
    if value < 0:
        value = ('{0:0' + str(bits) + 'b}').format((1 << bits) + value)
    else:
        if (value & (1 << (bits - 1))) != 0:
            value = value - (1 << bits)
        value = ('{0:0' + str(bits) + 'b}').format(value)
    return value

def litBreak(value):
    if type(value)==str:
        if value[0]=='#':
            value = int(value[1:])
        else:
            value = int(ord(value[1]))
    destination = makeBinary(value)
    one = destination[:8]
    two = destination[8:16]
    three = destination[16:24]
    four = destination[24:]
    return [one,two,three,four]

def addInstruction(mem,vals,line):
    toCode(line)
    for i in range(8):
        mem.append(address.Address())
        mem[-1].set(vals[i])
        
def toCode(line):
    if firstInstruction[0] == -1:
        firstInstruction[0] = line-1
    
def labelIsInstruction(l, label, labels, error):
    if labels[label] < firstInstruction[0]:
        return False
    return True

def labelIsDirective(l, label, labels):
    if labels[label] >= firstInstruction:
        return False
    return True
        
def isRegister(l, name):
    if not name or name[0].upper() != 'R' or name.upper() not in registers:
        return False
    return True

def isLabel(l, name, labels):
    if not name or name not in labels:
        return False
    return True

def isInteger(l, name):
    if not name or name[0] != '#' or not name[1:].lstrip('-').isdigit():
        return False
    return True

def tokenify(lines):
    error = ''
    oLines = lines
    oLines = [o.split(';')[0] for o in oLines if o.split(';')[0].strip()]
    lines = [l.split(';')[0] for l in lines if l.split(';')[0].strip()]
    retlines = []
    # Directives and label dictionary
    for l in lines:
        line = shlex.split(l, posix=False)
        if (label := re.search("^[a-zA-Z0-9][a-zA-Z0-9_]*", line[0])) and line[0].upper() not in instructions.__members__:
            label = label[0]
            if len(line) < 2:
                error+='Invalid syntax in "' + l + '"  labels cannot be on otherwise empty line.\n'
                continue
            operator = line[1].upper()
            if len(line) > 2:
                if line[2] in registers:
                    operand1 = line[2].upper() if line[2][0] != "'" else line[2]
                else:
                    operand1 = line[2] if line[2][0] != "'" else line[2]
            else:
                operand1 = None
            if len(line)>3:
                if line[3] in registers:
                    operand2 = line[3].upper() if line[3][0] != "'" else line[3]
                else:
                    operand2 = line[3] if line[3][0] != "'" else line[3]
            else:
                operand2 = None
            if len(line) > 4:
                if line[4] in registers:
                    operand3 = line[4].upper() if line[4][0] != "'" else line[4]
                else:
                    operand3 = line[4] if line[4][0] != "'" else line[4]
            else:
                operand3 = None
        else:
            label = None
            operator = line[0].upper()
            if len(line) > 1:
                if line[1] in registers:
                    operand1 = line[1].upper() if line[1][0] != "'" else line[1]
                else:
                    operand1 = line[1] if line[1][0] != "'" else line[1]
            else:
                operand1 = None
            if len(line)>2:
                if line[2] in registers:
                    operand2 = line[2].upper() if line[2][0] != "'" else line[2]
                else:
                    operand2 = line[2] if line[2][0] != "'" else line[2]
            else:
                operand2 = None
            if len(line)>3:
                if line[3] in registers:
                    operand3 = line[3].upper() if line[3][0] != "'" else line[3]
                else:
                    operand3 = line[3] if line[3][0] != "'" else line[3]
            else:
                operand3 = None
        retlines.append([label, operator, operand1, operand2, operand3])
    return [oLines, retlines, error]

def readInstruction(memory, registers,error):
    if registers['pc'].getInt() >= len(memory)-7 or registers['pc'].getInt() < 0:
        error+='PC out of bounds: ' + str(registers['pc'].getInt())
        return 0,0,0,0,0,error
    instRegs = memory[registers['pc'].getInt():registers['pc'].getInt()+8]
    operator = instRegs[0].getInt()
    operand1 = instRegs[1].getInt()
    operand2 = instRegs[2].getInt()
    operand3 = instRegs[3].getInt()
    immediate = int(instRegs[4].get() + instRegs[5].get() + instRegs[6].get() + instRegs[7].get(),2)
    return operator, operand1, operand2, operand3, immediate, error

def assemble(lines):
    olines,slines, error = tokenify(lines)
    if error:
        return [],[],[],{}, error
    # Directive and labels
    labels = {}
    lineNo = 0
    for l,line in zip(lines,slines):
        label, operator, operand1, operand2, operand3 = line
        if label: 
            if label in labels:
                error+='\nDuplicate label: ' + label + '\n'
                return [],[],[],{}, error
            else:
             labels[label] = lineNo
        if operator[0] == '.' and operator[1:] in directives.__members__:
            if firstInstruction[0]!=-1:
                error+='"' + l + '" not in data section...\n'
            match operator[1:]:
                case "INT":
                    if not isInteger(l, operand1):
                        error+='Invalid syntax in "' + l + '"  INT data must be a number. example: ".INT #12"\n'
                    lineNo+=3
                case "BYT":
                    if operand1:
                        if operand1[0] != "'" and operand1[0] != "#":
                            error+='Invalid syntax in "' + l + '"  BYT data must be character, number, or blank. examples: ".BYT \'a\'", ".BYT #12", ".BYT"\n'
                        elif operand1[0] == "'":
                            if not operand1[2] == "'":
                                error+='Invalid syntax in "' + l + '"  BYT data characters must be a single character in single quotes. example: ".BYT \'a\'"\n'
                        elif operand1[0] == '#':
                            if  not operand1[1:].isdigit():
                                error+='Invalid syntax in "' + l + '"  BYT data numbers must have a pound and number as operand1 operand.  example: ".BYT #12"\n'
                            if int(operand1[1:]) < 0 or int(operand1[1:]) > 255:
                                error+='Invalid syntax in "' + l + '"  BYT data numbers must be in range 0-255.  example: ".BYT #12"\n'
                case "BTS":
                    if not operand1 or operand1[0] != '#' or not operand1[1:].isdigit():
                        error+='Invalid syntax in "' + l + '"  BTS data must have pound then an unsigned number as operand1 operand. example: ".BTS #12"\n'
                        return [],[],[],{}, error
                    lineNo+=int(operand1[1:])-1
                case "STR":
                    if not operand1:
                        error+='Invalid syntax in "' + l + '"  STR data must have string or string length as operand1 operand. examples: ".STR \'hello\'", ".STR #12"\n'
                    elif operand1[0] == '#':
                        if not operand1[1:].lstrip('-').isdigit():
                            error+='Invalid syntax in "' + l + '"  STR data numbers must have a pound and number as operand1 operand.  example: ".STR #12"\n'
                    elif operand1[0] == '"':
                        if not re.search("\"[\\[\\]a-zA-Z0-9!@#$%^&*)(+\\-_=?<>}{\\,./:; \"`~]*\"", operand1):
                            error+='Invalid syntax in "' + l + '"  STR data must be string in double quotes. examples: ".STR "hello""\n'
                    else:
                        error+='Invalid syntax in "' + l + '"  STR data operand must be string or string length. examples: ".STR "hello"", ".STR #12"\n'
                    lineNo+=len(operand1)-1
        if operator in instructions.__members__:
            toCode( lineNo +1)
            lineNo+=7
        lineNo+=1
    if 'MAIN' not in labels:
        error+='Invalid syntax in "' + l + '"  MAIN instruction missing.\n'
    # Instruction
    if error:
        # sys.stderr.write(error)
        return None, olines, slines, labels, error
    for (oline,sline) in zip(olines,slines):
        _, operator, operand1, operand2, operand3 = sline
        if operator in instructions.__members__:
            match operator:
                case "JMP":                                                         #  label
                    if not isLabel(oline, operand1, labels):
                        error += operator + ' operator must be followed by label.\n'
                case "JMR" | 'PSHR' | 'PSHB' | 'POPR' | 'POPB':                     # register 
                    if not isRegister(oline,operand1):
                        error += operator + ' operator must be followed by register.\n'
                case "BNZ" | "BGT" | "BLT" | "BRZ":                                 # register | label
                    if not isRegister(oline,operand1) or not isLabel(oline, operand2, labels):
                        error += operator + ' operator must be followed by a register then a label.\n'
                case 'MOV' | 'IALLC' | 'ISTR' | 'ISTB' | 'ILDB' | 'ILDR':   # register | register 
                    if not isRegister(oline,operand1) or not isRegister(oline,operand2):
                        error += operator + ' must be followed by two registers.\n'
                case 'ADD' | 'SUB' | 'MUL' | 'DIV' | 'SDIV' | 'AND' | 'OR' | 'CMP': # register | register | register
                    if not isRegister(oline,operand1) or not isRegister(oline,operand2) or not isRegister(oline, operand3):
                        error += operator + ' must be followed by three registers.\n'
                case 'ADDI' | 'MULI' | 'DIVI' |  'CMPI' | 'SUBI':                   # register | register | Num
                    if not isRegister(oline,operand1) or not isRegister(oline,operand2) or not isInteger(oline, operand3):
                        error += operator + ' must be followed by two registers and a number.\n'
                case 'TRP':                                                         # integer
                    if not isInteger(oline, operand1):
                        error += operator + ' must be followed by a number.\n'
                case 'STR' | 'LDR' | 'LDB' | 'STB' | 'LDA' | 'ALLC':                # register label
                    if not isRegister(oline,operand1) or not isLabel(oline, operand2, labels):
                        error += operator + ' must be followed by a register and a label.\n'
                case 'MOVI' | 'ALCI':                                               # register | Num
                    if not isRegister(oline,operand1) or not isInteger(oline, operand2):
                        error += operator + ' must be followed by a register and a number.\n'
                case 'CALL':                                                        # label
                    if not isLabel(oline, operand1, labels):
                        error += operator + ' must be followed by a label.\n'
            if error:
                return [],[],[],{}, error
        
    # Build Memory
    memory = []
    firstInstruction[0] = -1
    for (oline,sline) in zip(olines,slines):

        label, operator, operand1, operand2, operand3 = sline
        match operator:
            case '.INT':
                binary = makeBinary(int(operand1[1:]))
                for n in range(4):
                    memory.append(address.Address())
                    memory[-1].set(binary[n*8:n*8+8],True)
                if operand1:
                    memory[-1].set(int(operand1[1:]))
            case '.BYT':
                memory.append(address.Address())
                if operand1:
                    if operand1[0] == "'":
                        memory[-1].set(ord(operand1[1]))
                    else:
                        memory[-1].set(int(operand1[1:]))
            case '.STR':
                memory.append(address.Address())
                if operand1[0] == '"':
                    memory[-1].set(len(operand1[1:-1]))
                    for c in operand1[1:-1]:
                        memory.append(address.Address())
                        memory[-1].set(ord(c))
                    memory.append(address.Address())
                else:
                    memory[-1].set(int(operand1[1:]))
                    for _ in range(int(operand1[1:])):
                        memory.append(address.Address())
                    memory.append(address.Address())
            case '.BTS':
                for n in range(int(operand1[1:])):
                    memory.append(address.Address())
            case 'JMP':
                addInstruction(memory,[1,0,0,0] + litBreak(labels[operand1]),len(memory)+1)
            case 'JMR'| 'PSHR' | 'PSHB' | 'POPR' | 'POPB':                                                                                  # Integer
                addInstruction(memory,[instructions.get(operator),int(operand1[1:]),0,0] + litBreak(0),len(memory)+1)
            case 'BNZ' | 'BGT' | 'BLT' | 'BRZ':                                                                                             # Integer | label
                addInstruction(memory,[instructions.get(operator),int(operand1[1:]),0,0] + litBreak(labels[operand2]),len(memory)+1)
            case 'MOV' | 'IALLC' | 'ISTR' | 'ISTB' | 'ILDB' | 'ILDR':                                                                       # Register, Register
                addInstruction(memory,[instructions.get(operator),int(operand1[1:]),int(operand2[1:]),0] + litBreak(0),len(memory)+1)
            case 'MOVI' | 'ALCI':                                                                                                           # Register | Num
                addInstruction(memory,[instructions.get(operator),int(operand1[1:]),0,0] + litBreak(operand2),len(memory)+1)
            case 'STR' | 'LDR' | 'LDB' | 'STB' | 'LDA' | 'ALLC':                                                                            # Register | label
                addInstruction(memory,[instructions.get(operator),int(operand1[1:]),0,0] + litBreak(labels[operand2]),len(memory)+1)
            case 'ADDI' | 'MULI' | 'DIVI' |  'CMPI' | 'SUBI':                                                                               # register, register | Num
                addInstruction(memory,[instructions.get(operator),int(operand1[1:]),int(operand2[1:]),0] + litBreak(operand3),len(memory)+1)
            case 'ADD' | 'SUB' | 'MUL' | 'DIV' | 'SDIV' | 'AND' | 'OR' | 'CMP':                                                             # register, register, register
                addInstruction(memory,[instructions.get(operator),int(operand1[1:]),int(operand2[1:]),int(operand3[1:])] + litBreak(0),len(memory)+1)
            case 'TRP':                                                                                                                    # |Integer
                addInstruction(memory,[instructions.get(operator),0,0,0] + litBreak(operand1), len(memory)+1)
            case 'CALL':                                                                                                                   # label
                addInstruction(memory,[instructions.get(operator),0,0,0] + litBreak(labels[operand1]), len(memory)+1)
            case 'RET':                                                                                                                    # |
                addInstruction(memory,[instructions.get(operator),0,0,0] + litBreak(0), len(memory)+1)

    registers['pc'].set(firstInstruction[0])
    registers['sb'].set(len(memory))
    registers['sp'].set(len(memory) + stackSize)
    registers['hp'].set(len(memory) + stackSize)
    registers['sl'].set(len(memory) + stackSize)
    return (memory,olines, slines, labels, error)

def emulate(memory,registers):
    error = ''
    while True:
        operator, operand1, operand2, operand3, immediate,error = readInstruction(memory, registers, error)
        if error:
            return (memory,error)
        inc = True
        match instructions.get(operator):
            case 'JMP':
                registers['pc'].set(immediate)
                inc = False
            case 'JMR':
                registers['pc'].set(registers['R'+str(operand1)].getInt())
                inc = False
            case 'BNZ':
                if registers['R'+str(operand1)].getInt():
                    registers['pc'].set(immediate)
                    inc = False
            case 'BGT':
                if registers['R'+str(operand1)].getInt() > registers['R'+str(operand2)].getInt():
                    registers['pc'].set(immediate)
                    inc = False
            case 'BLT':
                if registers['R'+str(operand1)].getInt() < registers['R'+str(operand2)].getInt():
                    registers['pc'].set(immediate)
                    inc = False
            case 'BRZ':
                if registers['R'+str(operand1)].getInt() == 0:
                    registers['pc'].set(immediate)
                    inc = False
            case 'ADDI':
                num = registers['R'+str(operand2)].getInt() + immediate
                registers['R'+str(operand1)].set(num)
            case 'TRP':
                match immediate:
                    case 0:
                        return (memory,error)
                    case 1:
                        sys.stdout.write(str(registers['R3'].getInt()))
                    case 2:
                        inp = input()
                        try:
                            registers['R3'].set(int(inp))
                        except:
                            error+='TRP 2: Invalid input: ' + inp + '\n'
                            return (memory,error)
                    case 3:
                        sys.stdout.write(registers['R3'].getChar())
                    case 4:
                        inp = input()
                        registers['R3'].set(ord(inp))                            
                    case 5:
                        num = memory[registers['R3'].getInt()].getInt()
                        for c in memory[registers['R3'].getInt()+1:registers['R3'].getInt()+num+1]:
                            sys.stdout.write(chr(c.getInt()))
                    case 6:
                        num = memory[registers['R3'].getInt()].getInt()
                        inp = input()
                        start = registers['R3'].getInt()+1
                        for i,c in enumerate(inp):
                            memory[start+i].set(ord(c))
                    case 98:
                        for r in registers:
                            sys.stdout.write(r + ': ' + registers[r].get() + '\n')
        if inc:
            registers['pc'].set(registers['pc'].getInt() + 8)
            inc = True

def main():
    if len(sys.argv) < 2:
        sys.stderr.write("Please specify a file to run next time...\n")
        return -1
    if os.path.exists(sys.argv[1]) == False:
        sys.stderr.write('File "' + sys.argv[1] + '" does not exist...\n')
        return -1
    with open(sys.argv[1], "r") as f:
        lines = f.readlines()
    memory, olines, slines, labels, error = assemble(lines)
    if error:
        sys.stderr.write(error)
        return error

    memory, error = emulate(memory, registers)
if __name__ == "__main__":
    main()
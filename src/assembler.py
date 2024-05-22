import sys
from enum import Enum
import re, shlex
try:
    import src.registers as regs
except:
    import registers as regs
try:
    import src.address as address
except:
    import address

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
    LDA = 8
    STR = 9
    LDR = 10
    STB = 11
    LDB = 12
    ADD = 13
    ADDI = 14
    SUB = 15
    MUL = 16
    DIV = 17
    AND = 18
    OR = 19
    CMP = 20
    TRP = 21
    ISTR = 22
    ILDR = 23
    ISTB = 24
    ILDB = 25
    MOVI = 31
    CMPI = 32
    MULI = 33
    DIVI = 34
    ALCI = 35
    ALLC = 36
    IALLC = 37
    SDIV = 38
    PSHR = 40
    PSHB = 41
    POPR = 42
    POPB = 43
    CALL = 44
    RET = 45

def makeBinary(value, bits=32):
    if value < 0:
        value = ('{0:0' + str(bits) + 'b}').format((1 << bits) + value)
    else:
        if (value & (1 << (bits - 1))) != 0:
            value = value - (1 << bits)
        value = ('{0:0' + str(bits) + 'b}').format(value)
    return value


def toCode(line):
    if firstInstruction[0] == -1:
        firstInstruction[0] = line
    
def labelIsInstruction(l, label, labels, error):
    if labels[label] < firstInstruction[0]:
        return 'Invalid syntax in "' + l + '" ' + label +' cannot jump to directives.\n'
    return ''

def labelIsDirective(l, label, labels):
    if labels[label] >= firstInstruction:
        return 'Invalid syntax in "' + l + '" ' + label +' cannot jump to instructions.\n'
    return ''
        
def isRegister(l, name):
    if not name or name[0].upper() != 'R' or name.upper() not in registers:
        return 'Invalid syntax in "' + l + '" ' + name +' instruction must have a valid register as operand1 operand.\n'
    return ''

def isLabel(l, name, labels):
    if not name or name not in labels:
        return 'Invalid syntax in "' + l + '" ' + name +' instruction must have a valid label as operand1 operand.\n'
    return ''

def isInteger(l, name):
    if not name or name[0] != '#' or not name[1:].lstrip('-').isdigit():
        return 'Invalid syntax in "' + l + '" ' + name +' INT data must have pound then number as operand1 operand.example: ".INT #-12" \n'
    return ''

def tokenify(lines):
    error = ''
    oLines = lines
    oLines = [o.split(';')[0] for o in oLines if o.split(';')[0].strip()]
    lines = [l.split(';')[0] for l in lines if l.split(';')[0].strip()]
    labels = {}
    retlines = []
    # Directives and label dictionary
    for i,l in enumerate(lines):
        line = shlex.split(l, posix=False)
        if (label := re.search("^[a-zA-Z0-9][a-zA-Z0-9_]*", line[0])) and line[0] not in instructions.__members__:
            label = label[0]
            if len(line) < 2:
                error+='Invalid syntax in "' + l + '"  labels cannot be on otherwise empty line.\n'
                continue
            if label in labels:
                error+='Invalid syntax in "' + l + '"  label "' + label + '" already used.\n'
            labels[label] = i+1
            operator = line[1].upper()
            if len(line) > 2:
                if line[2] in registers:
                    operand1 = line[2].upper() if line[2][0] != "'" else line[2]
                else:
                    operand1 = line[2] if line[2][0] != "'" else line[2]
            else:
                operand1 = None
            if len(line)>=4:
                if line[3] in registers:
                    operand2 = line[3].upper() if line[3][0] != "'" else line[3]
                else:
                    operand2 = line[3] if line[3][0] != "'" else line[3]
            else:
                operand2 = None
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
        retlines.append([label, operator, operand1, operand2])
    return [oLines, retlines, labels, error]
        
def assemble(lines):
    olines,slines, labels, error = tokenify(lines)
    if error:
        sys.stderr.write(error)
        exit(1)
    # Directive 
    for i,(l,line) in enumerate(zip(lines,slines)):
        _, operator, operand1, operand2 = line
        if operator[0] == '.' and operator[1:] in directives.__members__:
            if firstInstruction[0]!=-1:
                print(firstInstruction)
                error+='"' + l + '" not in data section...\n'
            match operator[1:]:
                case "INT":
                    error += isInteger(l, operand1)
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
        if operator in instructions.__members__:
            toCode( i +1)
    if 'MAIN' not in labels:
        error+='Invalid syntax in "' + l + '"  MAIN instruction missing.\n'
    # Instruction
    if error:
        sys.stderr.write(error)
        return None, olines, slines, labels, error
    for (oline,sline) in zip(olines,slines):
        _, operator, operand1, operand2 = sline
        if operator in instructions.__members__:
            match operator:
                case "JMP":
                    error += isLabel(l, operand1, labels)
                    error += labelIsInstruction(l, operand1, labels, error)
                case "JMR" | 'PSHR' | 'PSHB' | 'POPR' | 'POPB':                                              # register
                    isRegister(l,operand1)
                case "BNZ" | "BGT" | "BLT" | "BRZ":                                                          # register | label to instruction
                    error += isRegister(l,operand1)
                    error += isLabel(l, operand2, labels)
                    error += labelIsInstruction(l,operand2, labels,error)
                case 'MOV' | 'ADD' | 'SUB' | 'MUL' | 'DIV' | 'AND' | 'OR' | 'CMP' | 'SDIV' | 'IALLC' | 'ISTR' | 'ISTB' | 'ILDB':        # register | register
                    error += isRegister(l,operand1)
                    error += isRegister(l,operand2)
                case 'ADDI' | 'MOVI' | 'MULI' | 'DIVI' |  'CMPI' | 'ALCI':                                    # register | integer
                    error += isRegister(l,operand1)
                    isInteger(l, operand2)
                case 'TRP':                                                                                  # integer
                    error += isInteger(l, operand1)
                case 'STR' | 'LDR' | 'LDB' | 'STB' | 'LDA' | 'ALLC':                                         # register | label
                    error += isRegister(l,operand1)
                    error += isLabel(l, operand2, labels)
                case 'CALL':
                    error += isLabel(l, operand1, labels)
    # Build Memory
    memory = []
    labels = {}
    for (oline,sline) in zip(olines,slines):
        label, operator, operand1, operand2 = sline
        if label:
            labels[label] = len(memory)
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
                    for c in operand1[1:]:
                        memory.append(address.Address())
                    memory.append(address.Address())
            case '.BTS':
                for n in range(int(operand1[1:])):
                    memory.append(address.Address())
            case 'JMP':
                memory.append(address.Address())
                memory[-1].set(1)
                for n in range(3): memory.append(address.Address())
    return (memory,olines, slines, labels, error)

def main():
    if len(sys.argv) < 2:
        error+="Please specify a file to run next time...\n"
        sys.exit(1)

    with open(sys.argv[1], "r") as f:
        lines = f.readlines()

    memory, olines, slines, labels, error = assemble(lines)
    if error:
        print(error)
        sys.stderr.write(error)
        return error
    




if __name__ == "__main__":
    main()
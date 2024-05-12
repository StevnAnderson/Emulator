import sys
from enum import Enum
import re, shlex
try:
    import src.registers as regs
except:
    import registers as regs

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
    if not name or name[0] != 'R' or name not in registers:
        return 'Invalid syntax in "' + l + '" ' + name +' instruction must have a valid register as second operand.\n'
    return ''

def isLabel(l, name, labels):
    if not name or name not in labels:
        return 'Invalid syntax in "' + l + '" ' + name +' instruction must have a valid label as second operand.\n'
    return ''

def isInteger(l, name):
    if not name or name[0] != '#' or not name[1:].lstrip('-').isdigit():
        return 'Invalid syntax in "' + l + '" ' + name +' INT data must have pound then number as second operand.example: ".INT #-12" \n'
    return ''

def assemble(lines):
    error = ''
    lines = [l.split(';')[0] for l in lines if l.split(';')[0].strip()]
    labels = {}
    # Directives and label dictionary
    for i,l in enumerate(lines):
        line = shlex.split(l, posix=False)
        if (label := re.search("^[a-zA-Z0-9][a-zA-Z0-9_]*", line[0])) and line[0] not in instructions.__members__:
            if len(line) < 2:
                error+='Invalid syntax in "' + l + '"  labels cannot be on otherwise empty line.\n'
                continue
            if label[0] in labels:
                error+='Invalid syntax in "' + l + '"  label "' + label[0] + '" already used.\n'
            labels[label[0].upper()] = i+1
            first = line[1].upper()
            if len(line) > 2:
                second = line[2].upper()
            else:
                second = None
            if len(line)>=4:
                third = line[3].upper()
            else:
                third = None
        else:
            first = line[0].upper()
            if len(line) > 1:
                second = line[1].upper()
            else:
                second = None
            if len(line)>2:
                third = line[2].upper()
            else:
                third = None
    # Directive 
        if first[0] == '.' and first[1:] in directives.__members__:
            if firstInstruction[0]!=-1:
                print(firstInstruction)
                error+='"' + l + '" not in data section...\n'
            match first[1:]:
                case "INT":
                    error += isInteger(l, second)
                case "BYT":
                    if second:
                        if second[0] != "'" and second[0] != "#":
                            error+='Invalid syntax in "' + l + '"  BYT data must be character, number, or blank. examples: ".BYT \'a\'", ".BYT #12", ".BYT"\n'
                        elif second[0] == "'" and not second[2] == "'":
                            error+='Invalid syntax in "' + l + '"  BYT data characters must be a single character in single quotes. example: ".BYT \'a\'"\n'
                        elif second[0] == '#' and not second[1:].lstrip('-').isdigit():
                            error+='Invalid syntax in "' + l + '"  BYT data numbers must have a pound and number as second operand.  example: ".BYT #12"\n'
                case "BTS":
                    if not second or second[0] != '#' or not second[1:].isdigit():
                        error+='Invalid syntax in "' + l + '"  BTS data must have pound then an unsigned number as second operand. example: ".BTS #12"\n'
                case "STR":
                    if not second:
                        error+='Invalid syntax in "' + l + '"  STR data must have string or string length as second operand. examples: ".STR \'hello\'", ".STR #12"\n'
                    elif second[0] == '#':
                        if not second[1:].lstrip('-').isdigit():
                            error+='Invalid syntax in "' + l + '"  STR data numbers must have a pound and number as second operand.  example: ".STR #12"\n'
                    elif second[0] == '"':
                        if not re.search("\"[\\[\\]a-zA-Z0-9!@#$%^&*)(+\\-_=?<>}{\\,./:; \"`~]*\"", second):
                            error+='Invalid syntax in "' + l + '"  STR data must be string in double quotes. examples: ".STR "hello""\n'
                    else:
                        error+='Invalid syntax in "' + l + '"  STR data operand must be string or string length. examples: ".STR "hello"", ".STR #12"\n'
        if first in instructions.__members__:
            toCode(i+1)
    if 'MAIN' not in labels:
        error+='Invalid syntax in "' + l + '"  MAIN instruction missing.\n'
    # Instruction
    for l in lines:
        line = shlex.split(l, posix=False)
        if (label := re.search("^[a-zA-Z0-9][a-zA-Z0-9_]*", line[0])) and line[0] not in instructions.__members__:
            first = line[1].upper()
            if len(line) > 2:
                second = line[2].upper()
            else:
                second = None
            if len(line)>=4:
                third = line[3].upper()
            else:
                third = None
        else:
            first = line[0].upper()
            if len(line) > 1:
                second = line[1].upper()
            else:
                second = None
            if len(line)>2:
                third = line[2].upper()
            else:
                third = None
        if first in instructions.__members__:
            match first:
                case "JMP":
                    error += isLabel(l, second, labels)
                    error += labelIsInstruction(l, second, labels, error)
                case "JMR" | 'PSHR' | 'PSHB' | 'POPR' | 'POPB':                                              # register
                    isRegister(l,second)
                case "BNZ" | "BGT" | "BLT" | "BRZ":                                                          # register | label to instruction
                    error += isRegister(l,second)
                    error += isLabel(l, third, labels)
                    error += labelIsInstruction(l,third, labels,error)
                case 'MOV' | 'ADD' | 'SUB' | 'MUL' | 'DIV' | 'AND' | 'OR' | 'CMP' | 'SDIV' | 'IALLC' | 'ISTR' | 'ISTB' | 'ILDB':        # register | register
                    error += isRegister(l,second)
                    error += isRegister(l,third)
                case 'ADDI' | 'MOVI' | 'MULI' | 'DIVI' |  'CMPI' | 'ALCI':                                    # register | integer
                    error += isRegister(l,second)
                    isInteger(l, third)
                case 'TRP':                                                                                  # integer
                    error += isInteger(l, second)
                case 'STR' | 'LDR' | 'LDB' | 'STB' | 'LDA' | 'ALLC':                                         # register | label
                    error += isRegister(l,second)
                    error += isLabel(l, third, labels)
                case 'CALL':
                    error += isLabel(l, second, labels)
    return (lines, labels, error)

def main():
    if len(sys.argv) < 2:
        error+="Please specify a file to run next time...\n"
        sys.exit(1)

    with open(sys.argv[1], "r") as f:
        lines = f.readlines()

    lines, labels, error = assemble(lines)
    if error:
        print(error)
        sys.stderr.write(error)
        return error
    




if __name__ == "__main__":
    main()
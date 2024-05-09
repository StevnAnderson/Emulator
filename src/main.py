import sys
from enum import Enum
import re
try:
    import src.registers as regs
except:
    import registers as regs

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
    if firstInstruction == -1:
        firstInstruction = line
    
registers = regs.registers
if len(sys.argv) < 2:
    input("Please specify a file to run next time...\nPress enter to exit.")
    sys.exit(1)

with open(sys.argv[1], "r") as f:
    lines = f.readlines()

lines = [l.split(';')[0] for l in lines if l.split(';')[0].strip()]
labels = {}
firstInstruction = -1
for i,l in enumerate(lines):
    line = l.split()
    if (label := re.search("^[a-zA-Z0-9][a-zA-Z0-9_]*", line[0])) and line[0] not in instructions.__members__:
        if len(line) < 2:
            input('Invalid syntax in "' + l + '"  label must have operand.\nPress enter to exit.')
        labels[label] = i+1
        first = line[1].upper()
        if len(line) > 2:
            second = line[2].upper()
        else:
            second = None
        if len(line)>4:
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
        if firstInstruction!=-1:
            input('"' + l + '" not in data section...\nPress enter to exit.')
            sys.exit(1)
        match first[1:]:
            case "INT":
                if not second or second[0] != '#' or not second[1:].lstrip('-').isdigit():
                    input('Invalid syntax in "' + l + '"  INT data must have pound then number as second operand.example: ".INT #-12" \nPress enter to exit.')
            case "BYT":
                if second:
                    if second[0] != "'" and not re.search("'.'", second):
                        input('Invalid syntax in "' + l + '"  BYT data characters must be a single character in single quotes. example: ".BYT \'a\'"\nPress enter to exit.')
                    elif second[0] == '#' and not second[1:].lstrip('-').isdigit():
                        input('Invalid syntax in "' + l + '"  BYT data numbers must have a pound and number as second operand.  example: ".BYT #12"\nPress enter to exit.')
                    else: 
                        input('Invalid syntax in "' + l + '"  BYT data must be character, number, or blank. examples: ".BYT \'a\'", ".BYT #12", ".BYT"\nPress enter to exit.')
            case "BTS":
                if not second or second[0] != '#' or not second[1:].lstrip('-').isdigit():
                    input('Invalid syntax in "' + l + '"  BTS data must have pound then number as second operand. example: ".BTS #12"\nPress enter to exit.')
            case "STR":
                if not second:
                    input('Invalid syntax in "' + l + '"  STR data must have string or string length as second operand. examples: ".STR \'hello\'", ".STR #12"\nPress enter to exit.')
                elif second[0] == '#' and not second[1:].lstrip('-').isdigit():
                    input('Invalid syntax in "' + l + '"  STR data numbers must have a pound and number as second operand.  example: ".STR #12"\nPress enter to exit.')
                elif second[0] != '"' and not re.search("\"[a-zA-Z0-9!@#$%^&*)\-+_=?<>\{\}\[\]\\,.\/:;( `~]*\"", second):
                    input('Invalid syntax in "' + l + '"  STR data must be string in double quotes. examples: ".STR "hello""\nPress enter to exit.')
                elif second[0] != '#' and not second[0] != '"':
                    input('Invalid syntax in "' + l + '"  STR data operand must be string or string length. examples: ".STR "hello"", ".STR #12"\nPress enter to exit.')
    if first in instructions.__members__:
        toCode(i+1)
# Instruction
for l in lines:
    if first in instructions.__members__:
        match first:
            case "JMP":
                if not second or second not in labels:
                    input('Invalid syntax in "' + l + '"  JMP instruction must have a valid label as second operand.\nPress enter to exit.')
            case "JMR":
                if not second or second not in registers:
                    input('Invalid syntax in "' + l + '"  JMR instruction must have a valid register as second operand.\nPress enter to exit.')
            case "BNZ":
                if not second or second not in registers:
                    input('Invalid syntax in "' + l + '"  BNZ instruction must have a valid register as second operand.\nPress enter to exit.')
                if not third or third not in labels:  
                    input('Invalid syntax in "' + l + '"  BNZ instruction must have a valid label as third operand.\nPress enter to exit.')              

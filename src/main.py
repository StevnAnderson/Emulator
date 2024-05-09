import sys
from enum import Enum
import re

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



if len(sys.argv) < 2:
    input("Please specify a file to run next time...\nPress enter to exit.")
    sys.exit(1)

with open(sys.argv[1], "r") as f:
    lines = f.readlines()

lines = [l.split(';')[0] for l in lines if l.split(';')[0].strip()]
dataSection = True
for l in lines:
    line = l.split()
    if (label := re.search("^[a-zA-Z0-9][a-zA-Z0-9_]*", line[0])) and line[0] not in instructions.__members__:
        first = line[1]
        if len(line) > 2:
            second = line[2]
        else:
            second = None
    else:
        first = line[0]
        if len(line) > 1:
            second = line[1]
        else:
            second = None        
# Directive 
    if first[0] == '.' and first[1:] in directives.__members__:
        if not dataSection:
            input('"' + l + '" not in data section...\nPress enter to exit.')
            sys.exit(1)
        match first[1:]:
            case "INT":
                if not second or second[0] != '#' or not second[1:].lstrip('-').isdigit():
                    input('Invalid syntax in "' + l + '"  INT data must have pound then number as second operand.example: ".INT #-12" \nPress enter to exit.')
            case "BYT":
                if second:
                    if second[0] != "'" and not re.search("'.'", second):
                        input('Invalid syntax in "' + l + '"  BYT data second operand must have number/character or be blank. examples: ".BYT #12", ".BYT \'a\'", ".BYT" \nPress enter to exit.')
                    if second[0] == '#' and not second[1:].lstrip('-').isdigit():
                        input('Invalid syntax in "' + l + '"  BYT data second operand must have number/character or be blank. examples: ".BYT #12", ".BYT \'a\'", ".BYT" \nPress enter to exit.')
                    if 
            case "BTS":
                pass
            case "STR":
                pass
    

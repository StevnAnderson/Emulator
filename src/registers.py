from enum import Enum

class Register():
    def __init__(self, name):
        self.name = name
        self.value = '{0:032b}'.format(0)
    
    def assign(self, value):
        if value.isdigit():
            self.value = '{0:032b}'.format(value)

    def get(self):
        return self.value
    
    def clear(self):
        self.value = '{0:032b}'.format(0)

registers =[
    Register('R0'),
    Register('R1'),
    Register('R2'),
    Register('R3'),
    Register('R4'), 
    Register('R5'),
    Register('R6'), 
    Register('R7'),
    Register('R8'),
    Register('R9'),
    Register('R10'),
    Register('R11'),
    Register('R12'),
    Register('R13'),
    Register('R14'),
    Register('R15'),
    Register('PC'),
    Register('SL'),
    Register('SB'),
    Register('SP'),
    Register('FP'),
    Register('HP') 
]


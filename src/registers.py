from enum import Enum

class Register():
    def __init__(self):
        self.value = '{0:032b}'.format(0)
    
    def set(self, value):
        if type(value)==int:
            self.value = '{0:032b}'.format(value)
        if type(value)==str:
            if value.isdigit():
                self.value = '{0:032b}'.format(int(value))

    def getInt(self):
        return int(self.value, 2)
    
    def getChar(self):
        n = self.getInt()
        if n > 255:
            return str(n)
        return chr(self.getInt())
    
    def get(self):
        return self.value
    
    def clear(self):
        self.value = '{0:032b}'.format(0)

registers = {
    'R0': Register(),
    'R1': Register(),
    'R2': Register(),
    'R3': Register(),
    'R4': Register(),
    'R5': Register(),
    'R6': Register(),
    'R7': Register(),
    'R8': Register(),
    'R9': Register(),
    'R10': Register(),
    'R11': Register(),
    'R12': Register(),
    'R13': Register(),
    'R14': Register(),
    'R15': Register(),
    'PC': Register(),
    'SL': Register(),
    'SB': Register(),
    'SP': Register(),
    'FP': Register(),
    'HP': Register()
}

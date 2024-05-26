from enum import Enum

class Register():
    def __init__(self, bits=32):
        self.nbits = bits
        self.value = ('{0:0' + str(self.nbits) + 'b}').format(0)
    
    def set(self, value, binary=False):
        if not binary:
            if type(value) == str:
                value = ord(value)
            if value < 0:
                self.value = ('{0:0' + str(self.nbits) + 'b}').format((1 << self.nbits) + value)
            else:
                if (value & (1 << (self.nbits - 1))) != 0:
                    value = value - (1 << self.nbits)
                self.value = ('{0:0' + str(self.nbits) + 'b}').format(value)
        else:
            if type(value) == str:
                if [x for x in value if x != '0' and x != '1']:
                    print('Invalid binary string "' + value + '"' )
                    return
                self.value = ('{0:0' + str(self.nbits) + 'b}').format(int(value,2))

    def getInt(self):
        if self.value[0] == '1':
            n = (int(self.value,2) - (1 << self.nbits))
            return (int(self.value,2) - (1 << self.nbits))
        else:
            return int(self.value, 2)
    
    def getChar(self):
        n = self.getInt()
        if n > 255:
            return str(n)
        return chr(self.getInt())
    
    def get(self):
        return self.value
    
    def clear(self):
        self.value = ('{0:0' + str(self.nbits) + 'b}').format(0)

    def getByte(self):
        return self.value[-8:]
    
    def setByte(self, value, binary=False):
        if not binary:
            if type(value) == int:
                if value < 0:
                    self.value = self.value[:-8] + ('{0:0' + str(8) + 'b}').format((1 << 8) + value)
                else:
                    if (value & (1 << (8 - 1))) != 0:
                        value = value - (1 << 8)
                    self.value = self.value[:-8] + ('{0:0' + str(8) + 'b}').format(value)
            elif type(value) == str:
                self.value = self.value[:-8] + ord(value)
        else:
            if type(value) == str:
                if [x for x in value if x != '0' and x != '1']:
                    print('Invalid binary string "' + value + '"' )
                    return
                self.value = self.value[:-8] + int(value,2)

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

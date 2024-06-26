import sys

class Address:
    def __init__(self, bits=8):
        self.nbits = bits
        self.value = ('{0:0' + str(bits) + 'b}').format(0)
    
    def set(self, value, binary=False):
        if not binary:
            if type(value) == int:
                if value < 0:
                    self.value = ('{0:0' + str(self.nbits) + 'b}').format((1 << self.nbits) + value)
                else:
                    if (value & (1 << (self.nbits - 1))) != 0:
                        value = value - (1 << self.nbits)
                    self.value = ('{0:0' + str(self.nbits) + 'b}').format(value)
            elif type(value) == str:
                self.set(value, True)
        else:
            if type(value) == str:
                if [x for x in value if x != '0' and x != '1']:
                    print('Invalid binary string "' + value + '"' )
                    return
                self.value = ('{0:0' + str(self.nbits) + 'b}').format(int(value,2))

    def get(self):
        return self.value

    def getChar(self):
        n = self.getInt()
        if n > 255:
            return str(n)
        return chr(self.getInt())

    def getInt(self):
        if self.value[0] == '1':
            return (int(self.value,2) - (1 << self.nbits))
        else:
            return int(self.value, 2)


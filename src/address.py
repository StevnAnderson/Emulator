import sys

class Address:
    def __init__(self, bits=32):
        self.value = '{0:032b}'.format(0)
        self.nbits = bits
    
    def set(self, value, binary=False):
        if not binary:
            if type(value) == str:
                value = int(value)
            if value < 0:
                self.value = '{0:032b}'.format((1 << self.nbits) + value)
            else:
                if (value & (1 << (self.nbits - 1))) != 0:
                    value = value - (1 << self.nbits)
                self.value = '{0:032b}'.format(value)
        else:
            if type(value) == str:
                if [x for x in value if x != '0' and x != '1']:
                    print('Invalid binary string "' + value + '"' )
                    return
                self.value = '{0:032}'.format(int(value))

    def get(self):
        return self.value
    
    def getInt(self):
        if self.value[0] == '1':
            return (int(self.value,2) - (1 << 32))
        else:
            return int(self.value, 2)


a = Address()
a.set('-5')
print(a.get())
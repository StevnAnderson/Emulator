import sys

class Address:
    def __init__(self, bits=8):
        self.value = ('{0:0' + str(bits) + 'b}').format(0)
        self.nbits = bits
    
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
                self.setByte(3, ord(value))
        else:
            if type(value) == str:
                if [x for x in value if x != '0' and x != '1']:
                    print('Invalid binary string "' + value + '"' )
                    return
                self.value = ('{0:0' + str(self.nbits) + 'b}').format(int(value))

    def get(self):
        return self.value
    
    def getByte(self, index):
        if index < 0 or index > 3 or not isinstance(index,int):
            print('Invalid byte index "' + str(index) + '"')
            return
        return self.value[index*4:index*4+4]
    
    def getAscii(self,value):
        return chr(int(self.getByte(3),2))

    def setByte(self, index, value):
        if index < 0 or index > 3 or not isinstance(index,int):
            print('Invalid byte index "' + str(index) + '"')
            return
        if len(value) > 8:
            print('Invalid byte length "' + str(len(value)) + '"')
            return
        if [x for x in value if x != '0' and x != '1']:
            print('Invalid binary string "' + value + '"' )
            return
        self.value = self.value[:index*8] + value + self.value[index*8+8:]

    def getInt(self):
        if self.value[0] == '1':
            return (int(self.value,2) - (1 << self.bits))
        else:
            return int(self.value, 2)


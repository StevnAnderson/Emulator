import sys

class Address:
    def __init__(self):
        self.value = '{0:096b}'.format(0)
    
    def set(self, value, binary=False):
        nbits = 96
        if not binary:
            if type(value) == int:
                if value < 0:
                    self.value = '{0:096b}'.format((1 << nbits) + value)
                else:
                    if (value & (1 << (nbits - 1))) != 0:
                        value = value - (1 << nbits)
                    self.value = '{0:096b}'.format(value)
        else:
            if type(value) == str:
                if [x for x in value if x != '0' and x != '1']:
                    print('Invalid binary string "' + value + '"' )
                    return
                self.value = '{0:096}'.format(int(value))

    def get(self):
        return self.value
    
    def getInt(self):
        if self.value[0] == '1':
            return (int(self.value,2) - (1 << 96))
        else:
            return int(self.value, 2)

def twos_complement(val, nbits):
    """Compute the 2's complement of int value val"""
    if val < 0:
        val = (1 << nbits) + val
    else:
        if (val & (1 << (nbits - 1))) != 0:
            # If sign bit is set.
            # compute negative value.
            val = val - (1 << nbits)
    return '{0:096b}'.format(val)

a = Address()
a.set('101', True)
print(a.getInt())
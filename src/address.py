import sys

class Address:
    def __init__(self):
        self.value = '{0:096b}'.format(0)
    
    def set(self, value):
        if type(value)==int:
            self.value = '{0:096b}'.format(value)
        if type(value)==str:
            if value.isdigit():
                self.value = '{0:096b}'.format(int(value))
            elif value[0] == '#' and value[1:].lstrip('-').isdigit():
                self.value = '{0:096b}'.format(int(value[1:]))

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

t = twos_complement(-2147483648, 96)
print(t, len([i for i in t if i == '0']))

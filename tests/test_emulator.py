import unittest, os, sys, io, builtins
from unittest.mock import patch
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
import vm
from contextlib import redirect_stdout


class TestEmulator(unittest.TestCase):

    def reset(self):
        vm.firstInstruction = [-1]
        [n.clear() for n in vm.registers.values()]

    def test_trp0(self):
        self.reset()
        testString = [
            "MAIN TRP #0"
        ]
        memory,lines, slines, labels, error = vm.assemble(testString)
        memory,error = vm.emulate(memory, vm.registers)
        self.assertEqual(error, '')

    def test_trp1(self):
        self.reset()
        sout = io.StringIO()
        testString = [
            'MAIN ADDI r3 r0 #1',
            "TRP #1",
            "TRP #0"
        ]
        memory,lines, slines, labels, error = vm.assemble(testString)
        self.assertEqual(error, '')
        with redirect_stdout(sout):
            memory,error = vm.emulate(memory, vm.registers)
        self.assertEqual(error, '')
        self.assertEqual(memory[0].getInt(), 19)
        self.assertEqual(memory[1].getInt(), 3)
        self.assertEqual(memory[2].getInt(), 0)
        self.assertEqual(memory[3].getInt(), 0)
        self.assertEqual(memory[4].getInt(), 0)
        self.assertEqual(memory[5].getInt(), 0)
        self.assertEqual(memory[6].getInt(), 0)
        self.assertEqual(memory[7].getInt(), 1)
        self.assertEqual(sout.getvalue(),'1')
        sout.close()

    def test_trp2(self):
        self.reset()
        testString = [
            "MAIN TRP #2",
            "TRP #0"
        ]
        memory,lines, slines, labels, error = vm.assemble(testString)
        with patch('builtins.input') as input_mock:
            input_mock.side_effect = ['10093223']
            memory,error = vm.emulate(memory, vm.registers)
        self.assertEqual(error, '')
        self.assertEqual(vm.registers['R3'].getInt(), 10093223)

    def test_trp3(self):
        self.reset()
        sout = io.StringIO()
        testString = [
            'MAIN ADDI r3 r0 #115',
            "TRP #3",
            "TRP #0"
        ]
        memory,lines, slines, labels, error = vm.assemble(testString)
        with redirect_stdout(sout):
            memory,error = vm.emulate(memory, vm.registers)
        t = sout.getvalue()
        self.assertEqual(error, '')
        self.assertEqual(memory[8].getInt(), 31)
        self.assertEqual(memory[15].getInt(), 3)
        self.assertEqual(memory[16].getInt(), 31)
        self.assertEqual(memory[17].getInt(), 0)
        self.assertEqual(vm.registers['R3'].getInt(), 115)
        self.assertEqual(sout.getvalue(),'s')
        sout.close()

    def test_trp4(self):
        self.reset()
        testString = [
            "MAIN TRP #4",
            "TRP #0"
        ]
        memory,lines, slines, labels, error = vm.assemble(testString)
        with patch('builtins.input') as input_mock:
            input_mock.side_effect = ['y']
            memory,error = vm.emulate(memory, vm.registers)
        self.assertEqual(error, '')
        self.assertEqual(vm.registers['R3'].getInt(), 121)
        self.assertEqual(memory[0].getInt(), 31)
        self.assertEqual(memory[1].getInt(), 0)
        self.assertEqual(memory[2].getInt(), 0)
        self.assertEqual(memory[3].getInt(), 0)
        self.assertEqual(memory[4].getInt(), 0)
        self.assertEqual(memory[5].getInt(), 0)
        self.assertEqual(memory[6].getInt(), 0)
        self.assertEqual(memory[7].getInt(), 4)
        self.assertEqual(memory[8].getInt(), 31)
        self.assertEqual(memory[15].getInt(), 0)

    def test_trp5(self):
        self.reset()
        testString = [
            'mystr .STR "hi there"',
            "MAIN TRP #5",
            "TRP #0"
        ]
        sout = io.StringIO()
        memory,lines, slines, labels, error = vm.assemble(testString)
        with redirect_stdout(sout):
            memory,error = vm.emulate(memory, vm.registers)
        self.assertEqual(error, '')
        self.assertEqual(memory[10].getInt(), 31)
        self.assertEqual(memory[17].getInt(), 5)
        self.assertEqual(vm.registers['R3'].getInt(), 0)
        self.assertEqual(sout.getvalue(),'hi there')
        sout.close()

    def test_trp6(self):
        self.reset()
        testString = [
            ".STR #5",
            "MAIN TRP #6",
            "TRP #0"
        ]
        memory,lines, slines, labels, error = vm.assemble(testString)
        with patch('builtins.input') as input_mock:
            input_mock.side_effect = ['Hello']
            memory,error = vm.emulate(memory, vm.registers)
        self.assertEqual(error, '')
        self.assertEqual(vm.registers['R3'].getInt(), 0)
        self.assertEqual(memory[0].getInt(), 5)
        self.assertEqual(memory[1].getInt(), 72)
        self.assertEqual(memory[2].getInt(), 101)
        self.assertEqual(memory[3].getInt(), 108)
        self.assertEqual(memory[4].getInt(), 108)
        self.assertEqual(memory[5].getInt(), 111)
        self.assertEqual(memory[6].getInt(), 0)
        self.assertEqual(memory[7].getInt(), 31)
        self.assertEqual(memory[14].getInt(), 6)

    def test_trp98(self):
        self.reset()
        testString = [
            'MAIN ADDI r0 r0 #0',
            "ADDI r1 r1 #1",
            "ADDI r2 r2 #2",
            "ADDI r3 r3 #3",
            "ADDI r4 r4 #4",
            "ADDI r5 r5 #5",
            "ADDI r6 r6 #6",
            "ADDI r7 r7 #7",
            "ADDI r8 r8 #8",
            "ADDI r9 r9 #9",
            "ADDI r10 r10 #10",
            "ADDI r11 r11 #11",
            "ADDI r12 r12 #12",
            "ADDI r13 r13 #13",
            "ADDI r14 r14 #14",
            "ADDI r15 r15 #15",
            "TRP #98",
            "TRP #0"
        ]
        memory,lines, slines, labels, error = vm.assemble(testString)
        sout = io.StringIO()
        with redirect_stdout(sout):
            memory,error = vm.emulate(memory, vm.registers)
        self.assertEqual(error, '')
        self.assertEqual(vm.registers['R0'].getInt(), 0)
        self.assertEqual(vm.registers['R1'].getInt(), 1)
        self.assertEqual(vm.registers['R2'].getInt(), 2)
        self.assertEqual(vm.registers['R3'].getInt(), 3)
        self.assertEqual(vm.registers['R4'].getInt(), 4)
        self.assertEqual(vm.registers['R5'].getInt(), 5)
        self.assertEqual(vm.registers['R6'].getInt(), 6)
        self.assertEqual(vm.registers['R7'].getInt(), 7)
        self.assertEqual(vm.registers['R8'].getInt(), 8)
        self.assertEqual(vm.registers['R9'].getInt(), 9)
        self.assertEqual(vm.registers['R10'].getInt(), 10)
        self.assertEqual(vm.registers['R11'].getInt(), 11)
        self.assertEqual(vm.registers['R12'].getInt(), 12)
        self.assertEqual(vm.registers['R13'].getInt(), 13)
        self.assertEqual(vm.registers['R14'].getInt(), 14)
        self.assertEqual(vm.registers['R15'].getInt(), 15)
        self.maxDiff = None
        self.assertEqual(sout.getvalue(),'''R0: 00000000000000000000000000000000
R1: 00000000000000000000000000000001
R2: 00000000000000000000000000000010
R3: 00000000000000000000000000000011
R4: 00000000000000000000000000000100
R5: 00000000000000000000000000000101
R6: 00000000000000000000000000000110
R7: 00000000000000000000000000000111
R8: 00000000000000000000000000001000
R9: 00000000000000000000000000001001
R10: 00000000000000000000000000001010
R11: 00000000000000000000000000001011
R12: 00000000000000000000000000001100
R13: 00000000000000000000000000001101
R14: 00000000000000000000000000001110
R15: 00000000000000000000000000001111
pc: 00000000000000000000000010000000
sl: 00000000000000000000001010000100
sb: 00000000000000000000000010010000
sp: 00000000000000000000001010000100
fp: 00000000000000000000000000000000
hp: 00000000000000000000001010000100
''')
        sout.close()

    def test_jmp(self):
        self.reset()
        testString = [
            "MAIN JMP end",
            "ADDI r0 r0 #1",
            "end TRP #0"
        ]
        memory,lines, slines, labels, error = vm.assemble(testString)
        memory,error = vm.emulate(memory, vm.registers)
        self.assertEqual(error, '')
        self.assertEqual(vm.registers['R0'].getInt(), 0)

    def test_jmr(self):
        self.reset()
        testString = [
            "MAIN ADDI r0 r0 #24",
            "JMR r0",
            "ADDI r0 r0 #1",
            "TRP #0"
        ]
        memory,lines, slines, labels, error = vm.assemble(testString)
        memory,error = vm.emulate(memory, vm.registers)
        self.assertEqual(error, '')
        self.assertEqual(vm.registers['R0'].getInt(), 24)


    def test_addi(self):
        self.reset()
        testString = [
            "MAIN ADDI r1 r1 #1",
            "ADDI r2 r1 #1",
            "TRP #0"
        ]
        memory,lines, slines, labels, error = vm.assemble(testString)
        memory,error = vm.emulate(memory, vm.registers)
        self.assertEqual(error, '')
        self.assertEqual(vm.registers['R0'].getInt(), 0)
        self.assertEqual(vm.registers['R1'].getInt(), 1)
        self.assertEqual(vm.registers['R2'].getInt(), 2)

    def test_bnz(self):
        self.reset()
        testString = [
            "MAIN ADDI r1 r0 #4",
            "BNZ r0 end",
            "MOV r0 r1",
            "end TRP #0"
        ]
        memory,lines, slines, labels, error = vm.assemble(testString)
        memory,error = vm.emulate(memory, vm.registers)
        self.assertEqual(error, '')
        self.assertEqual(vm.registers['R0'].getInt(), 0)
        self.reset()
        testString = [
            "MAIN BNZ r0 end",
            "ADDI r0 r0 #1",
            "end TRP #0"
        ]
        memory,lines, slines, labels, error = vm.assemble(testString)
        memory,error = vm.emulate(memory, vm.registers)
        self.assertEqual(error, '')
        self.assertEqual(vm.registers['R0'].getInt(), 1)

    def test_bgt(self):
        self.reset()
        testString = [
            "MAIN ADDI r1 r1 #1",
            "BGT r1 end",
            "ADDI r1 r1 #1",
            "end TRP #0"
        ]
        memory,lines, slines, labels, error = vm.assemble(testString)
        memory,error = vm.emulate(memory, vm.registers)
        self.assertEqual(error, '')
        self.assertEqual(vm.registers['R1'].getInt(), 1)

    def test_blt(self):
        self.reset()
        testString = [
            "MAIN ADDI r1 r1 #-1",
            "BLT r1 end",
            "ADDI r2 r2 #1",
            "end TRP #0"
        ]
        memory,lines, slines, labels, error = vm.assemble(testString)
        memory,error = vm.emulate(memory, vm.registers)
        self.assertEqual(error, '')
        self.assertEqual(vm.registers['R1'].getInt(), -1)
        self.assertEqual(vm.registers['R2'].getInt(), 0)

if __name__ == '__main__':
    t = TestEmulator()
    # t.test_jmr()
    ml = [func for func in dir(TestEmulator) if callable(getattr(TestEmulator, func)) and func.startswith('test_')]
    for func in ml:
        eval(f't.{func}()')

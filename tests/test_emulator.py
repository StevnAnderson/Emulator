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
        t = sout.getvalue()
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
        self.assertEqual(memory[0].getInt(), 19)
        self.assertEqual(memory[1].getInt(), 3)
        self.assertEqual(memory[2].getInt(), 0)
        self.assertEqual(memory[3].getInt(), 0)
        self.assertEqual(memory[4].getInt(), 0)
        self.assertEqual(memory[5].getInt(), 0)
        self.assertEqual(memory[6].getInt(), 0)
        self.assertEqual(memory[7].getInt(), 115)
        self.assertEqual(vm.registers['R3'].getInt(), 115)
        self.assertEqual(sout.getvalue(),'s')

    def test_addi(self):
        self.reset()
        testString = [
            "MAIN ADDI r0 r0 #1",
            "TRP #0"
        ]
        memory,lines, slines, labels, error = vm.assemble(testString)
        memory,error = vm.emulate(memory, vm.registers)
        self.assertEqual(error, '')
        self.assertEqual(vm.registers['R0'].getInt(), 1)



if __name__ == '__main__':
    t = TestEmulator()
    # t.test_trp3()
    ml = [func for func in dir(TestEmulator) if callable(getattr(TestEmulator, func)) and func.startswith('test_')]
    for func in ml:
        eval(f't.{func}()')

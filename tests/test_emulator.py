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
        self.assertEqual(error, '')
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
sl: 00000000000000000000000010010000
sb: 00000000000000000000001010000011
sp: 00000000000000000000000010010000
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
        self.assertEqual(error, '')
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
        self.assertEqual(error, '')
        memory,error = vm.emulate(memory, vm.registers)
        self.assertEqual(error, '')
        self.assertEqual(vm.registers['R0'].getInt(), 24)

    def test_bnz(self):
        self.reset()
        testString = [
            "MAIN ADDI r0 r0 #4",
            "BNZ r0 end",
            "MOV r0 r1",
            "end TRP #0"
        ]
        memory,lines, slines, labels, error = vm.assemble(testString)
        self.assertEqual(error, '')
        memory,error = vm.emulate(memory, vm.registers)
        self.assertEqual(error, '')
        self.assertEqual(vm.registers['R0'].getInt(), 4)
        self.reset()
        testString = [
            "MAIN BNZ r0 end",
            "ADDI r0 r0 #1",
            "end TRP #0"
        ]
        memory,lines, slines, labels, error = vm.assemble(testString)
        self.assertEqual(error, '')
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
        self.assertEqual(error, '')
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
        self.assertEqual(error, '')
        memory,error = vm.emulate(memory, vm.registers)
        self.assertEqual(error, '')
        self.assertEqual(vm.registers['R1'].getInt(), -1)
        self.assertEqual(vm.registers['R2'].getInt(), 0)

    def test_brz(self):
        self.reset()
        testString = [
            "MAIN BRZ r1 end",
            "ADDI r2 r2 #1",
            "end TRP #0"
        ]
        memory,lines, slines, labels, error = vm.assemble(testString)
        self.assertEqual(error, '')            
        memory,error = vm.emulate(memory, vm.registers)
        self.assertEqual(error, '')
        self.assertEqual(vm.registers['R1'].getInt(), 0)
        self.assertEqual(vm.registers['R2'].getInt(), 0)
        self.reset()
        testString = [
            "MAIN ADDI r1 r1 #1",
            "BRZ r1 end",
            "ADDI r2 r2 #1",
            "end TRP #0"
        ]
        memory,lines, slines, labels, error = vm.assemble(testString)
        self.assertEqual(error, '')
        memory,error = vm.emulate(memory, vm.registers)
        self.assertEqual(error, '')
        self.assertEqual(vm.registers['R1'].getInt(), 1)
        self.assertEqual(vm.registers['R2'].getInt(), 1)

    def test_mov(self):
        self.reset()
        testString = [
            "MAIN ADDI r0 r0 #1",
            "MOV r1 r0",
            "TRP #0"
        ]
        memory,lines, slines, labels, error = vm.assemble(testString)
        self.assertEqual(error, '')
        memory,error = vm.emulate(memory, vm.registers)
        self.assertEqual(error, '')
        self.assertEqual(vm.registers['R0'].getInt(), 1)
        self.assertEqual(vm.registers['R1'].getInt(), 1)

    def test_movi(self):
        self.reset()
        testString = [
            "MAIN MOVI r0 #1",
            "TRP #0"
        ]
        memory,lines, slines, labels, error = vm.assemble(testString)
        self.assertEqual(error, '')
        memory,error = vm.emulate(memory, vm.registers)
        self.assertEqual(error, '')
        self.assertEqual(vm.registers['R0'].getInt(), 1)

    def test_lda(self):
        self.reset()
        testString = [
            "MAIN LDA r2 end",
            "end TRP #0"
        ]
        memory,lines, slines, labels, error = vm.assemble(testString)
        self.assertEqual(error, '')
        memory,error = vm.emulate(memory, vm.registers)
        self.assertEqual(error, '')
        self.assertEqual(vm.registers['R0'].getInt(), 0)
        self.assertEqual(vm.registers['R1'].getInt(), 0)
        self.assertEqual(vm.registers['R2'].getInt(), 8)

    def test_str(self):
        self.reset()
        testString = [
            "myint .INT #0",
            "MAIN ADDI r0 r0 #1",
            "STR r0 myint",
            "end TRP #0"
        ]
        memory,lines, slines, labels, error = vm.assemble(testString)
        self.assertEqual(error, '')
        memory,error = vm.emulate(memory, vm.registers)
        self.assertEqual(error, '')
        self.assertEqual(memory[3].getInt(), 1)

    def test_ldr(self):
        self.reset()
        testString = [
            "myint .INT #1",
            "MAIN LDR r0 myint",
            "end TRP #0"
        ]
        memory,lines, slines, labels, error = vm.assemble(testString)
        self.assertEqual(error, '')
        memory,error = vm.emulate(memory, vm.registers)
        self.assertEqual(error, '')
        self.assertEqual(vm.registers['R0'].getInt(), 0)

    def test_istr(self):
        self.reset()
        testString = [
            "WRITER .INT #24",
            "MAIN LDA R2 WRITER",
            "ADDI r1 R1 #1",
            "ISTR R1 R2",
            "TRP #0"
        ]
        memory,lines, slines, labels, error = vm.assemble(testString)
        self.assertEqual(error, '')
        memory,error = vm.emulate(memory, vm.registers)
        self.assertEqual(error, '')
        self.assertEqual(memory[0].getInt(), 0)
        self.assertEqual(memory[1].getInt(), 0)
        self.assertEqual(memory[2].getInt(), 0)
        self.assertEqual(memory[3].getInt(), 1)

    def test_ildr(self):
        self.reset()
        testString = [
            "READER .INT #24",
            "read .INT #14",
            "MAIN LDA R2 read",
            "ILDR R1 R2",
            "TRP #0"
        ]
        memory,lines, slines, labels, error = vm.assemble(testString)
        self.assertEqual(error, '')
        memory,error = vm.emulate(memory, vm.registers)
        self.assertEqual(error, '')
        self.assertEqual(vm.registers['R1'].getInt(), 14)

    def test_istb(self):
        self.reset()
        testString = [
            "WRITER .BYT",
            "MAIN LDA R2 WRITER",
            "ADDI r1 R1 #-1",
            "ISTB R1 R2",
            "TRP #0"
        ]
        memory,lines, slines, labels, error = vm.assemble(testString)
        self.assertEqual(error, '')
        memory,error = vm.emulate(memory, vm.registers)
        self.assertEqual(error, '')
        self.assertEqual(memory[0].getInt(), -1)
        self.assertEqual(memory[1].getInt(), 9)

    def test_ildb(self):
        self.reset()
        testString = [
            "READER .BYT",
            "read .BYT #12",
            "MAIN LDA R2 read",
            "ILDB R1 R2",
            "TRP #0"
        ]
        memory,lines, slines, labels, error = vm.assemble(testString)
        self.assertEqual(error, '')
        memory,error = vm.emulate(memory, vm.registers)
        self.assertEqual(error, '')
        self.assertEqual(vm.registers['R1'].getInt(), 12)

    def test_add(self):
        self.reset()
        testString = [
            "MAIN ADDI r0 r0 #1",
            "ADD r4 r1 r0",
            "TRP #0"
        ]
        memory,lines, slines, labels, error = vm.assemble(testString)
        self.assertEqual(error, '')
        memory,error = vm.emulate(memory, vm.registers)
        self.assertEqual(error, '')
        self.assertEqual(vm.registers['R4'].getInt(), 1)
        self.assertEqual(vm.registers['R0'].getInt(), 1)
        self.assertEqual(vm.registers['R1'].getInt(), 0)

    def test_addi(self):
        self.reset()
        testString = [
            "MAIN ADDI r1 r1 #1",
            "ADDI r2 r1 #1",
            "TRP #0"
        ]
        memory,lines, slines, labels, error = vm.assemble(testString)
        self.assertEqual(error, '')
        memory,error = vm.emulate(memory, vm.registers)
        self.assertEqual(error, '')
        self.assertEqual(vm.registers['R0'].getInt(), 0)
        self.assertEqual(vm.registers['R1'].getInt(), 1)
        self.assertEqual(vm.registers['R2'].getInt(), 2)

    def test_sub(self):
        self.reset()
        testString = [
            "MAIN ADDI r0 r0 #1",
            "SUB r4 r1 r0",
            "TRP #0"
        ]
        memory,lines, slines, labels, error = vm.assemble(testString)
        self.assertEqual(error, '')
        memory,error = vm.emulate(memory, vm.registers)
        self.assertEqual(error, '')
        self.assertEqual(vm.registers['R4'].getInt(), -1)

    def test_subi(self):
        self.reset()
        testString = [
            "MAIN ADDI r1 r1 #4",
            "SUBI r2 r1 #1",
            "TRP #0"
        ]
        memory,lines, slines, labels, error = vm.assemble(testString)
        self.assertEqual(error, '')
        memory,error = vm.emulate(memory, vm.registers)
        self.assertEqual(error, '')
        self.assertEqual(vm.registers['R0'].getInt(), 0)
        self.assertEqual(vm.registers['R1'].getInt(), 4)
        self.assertEqual(vm.registers['R2'].getInt(), 3)

    def test_mul(self):
        self.reset()
        testString = [
            "MAIN ADDI r0 r0 #1",
            "MUL r4 r1 r0",
            "TRP #0"
        ]
        memory,lines, slines, labels, error = vm.assemble(testString)
        self.assertEqual(error, '')
        memory,error = vm.emulate(memory, vm.registers)
        self.assertEqual(error, '')
        self.assertEqual(vm.registers['R4'].getInt(), 0)
    
    def test_muli(self):
        self.reset()
        testString = [
            "MAIN ADDI r1 r1 #2",
            "MULI r3 r1 #3",
            "TRP #0"
        ]
        memory,lines, slines, labels, error = vm.assemble(testString)
        self.assertEqual(error, '')
        memory,error = vm.emulate(memory, vm.registers)
        self.assertEqual(error, '')
        self.assertEqual(vm.registers['R0'].getInt(), 0)
        self.assertEqual(vm.registers['R1'].getInt(), 2)
        self.assertEqual(vm.registers['R2'].getInt(), 0)
        self.assertEqual(vm.registers['R3'].getInt(), 6)
    
    def test_div(self):
        self.reset()
        testString = [
            "MAIN ADDI r1 r1 #2",
            'addi r2 r2 #6',
            "DIV r3 r2 r1",
            "TRP #0"
        ]
        memory,lines, slines, labels, error = vm.assemble(testString)
        self.assertEqual(error, '')
        memory,error = vm.emulate(memory, vm.registers)
        self.assertEqual(error, '')
        self.assertEqual(vm.registers['R0'].getInt(), 0)
        self.assertEqual(vm.registers['R1'].getInt(), 2)
        self.assertEqual(vm.registers['R2'].getInt(), 6)
        self.assertEqual(vm.registers['R3'].getInt(), 3)

    def test_sdiv(self):
        self.reset()
        testString = [
            "MAIN ADDI r1 r1 #2",
            'addi r2 r2 #6',
            "DIV r3 r2 r1",
            "TRP #0"
        ]
        memory,lines, slines, labels, error = vm.assemble(testString)
        self.assertEqual(error, '')
        memory,error = vm.emulate(memory, vm.registers)
        self.assertEqual(error, '')
        self.assertEqual(vm.registers['R0'].getInt(), 0)
        self.assertEqual(vm.registers['R1'].getInt(), 2)
        self.assertEqual(vm.registers['R2'].getInt(), 6)
        self.assertEqual(vm.registers['R3'].getInt(), 3)

    def test_divi(self):
        self.reset()
        testString = [
            "MAIN ADDI r1 r1 #6",
            "DIVI r3 r1 #3",
            "TRP #0"
        ]
        memory,lines, slines, labels, error = vm.assemble(testString)
        self.assertEqual(error, '')
        memory,error = vm.emulate(memory, vm.registers)
        self.assertEqual(error, '')
        self.assertEqual(vm.registers['R0'].getInt(), 0)
        self.assertEqual(vm.registers['R1'].getInt(), 6)
        self.assertEqual(vm.registers['R2'].getInt(), 0)
        self.assertEqual(vm.registers['R3'].getInt(), 2)

    def test_and(self):
        self.reset()
        testString = [
            "MAIN ADDI r2 r2 #5",
            "ADDI r1 r1 #21",
            "AND r0 r2 r1",
            "TRP #0"
        ]
        memory,lines, slines, labels, error = vm.assemble(testString)
        self.assertEqual(error, '')
        memory,error = vm.emulate(memory, vm.registers)
        self.assertEqual(error, '')
        self.assertEqual(vm.registers['R0'].getInt(), 5)
        self.assertEqual(vm.registers['R1'].getInt(), 21)
        self.assertEqual(vm.registers['R2'].getInt(), 5)
        self.assertEqual(vm.registers['R3'].getInt(), 0)

    def test_or(self):
        self.reset()
        testString = [
            "MAIN ADDI r2 r2 #5",
            "ADDI r1 r1 #2",
            "OR r0 r2 r1",
            "TRP #0"
        ]
        memory,lines, slines, labels, error = vm.assemble(testString)
        self.assertEqual(error, '')
        memory,error = vm.emulate(memory, vm.registers)
        self.assertEqual(error, '')
        self.assertEqual(vm.registers['R0'].getInt(), 7)
        self.assertEqual(vm.registers['R1'].getInt(), 2)
        self.assertEqual(vm.registers['R2'].getInt(), 5)
        self.assertEqual(vm.registers['R3'].getInt(), 0)

    def test_cmp(self):
        self.reset()
        testString = [
            "MAIN ADDI r2 r2 #5",
            "ADDI r1 r1 #2",
            "CMP r0 r2 r1",
            "TRP #0"
        ]
        memory,lines, slines, labels, error = vm.assemble(testString)
        self.assertEqual(error, '')
        memory,error = vm.emulate(memory, vm.registers)
        self.assertEqual(error, '')
        self.assertEqual(vm.registers['R0'].getInt(), 1)
        self.assertEqual(vm.registers['R1'].getInt(), 2)
        self.assertEqual(vm.registers['R2'].getInt(), 5)
        self.assertEqual(vm.registers['R3'].getInt(), 0)
        self.reset()
        testString = [
            "MAIN ADDI r2 r2 #2",
            "ADDI r1 r1 #1",
            "CMP r0 r1 r2",
            "TRP #0"
        ]
        memory,lines, slines, labels, error = vm.assemble(testString)
        self.assertEqual(error, '')
        memory,error = vm.emulate(memory, vm.registers)
        self.assertEqual(error, '')
        self.assertEqual(vm.registers['R0'].getInt(), -1)
        self.assertEqual(vm.registers['R1'].getInt(), 1)
        self.assertEqual(vm.registers['R2'].getInt(), 2)
        self.reset()
        testString = [
            "MAIN ADDI r2 r2 #2",
            "ADDI r1 r1 #2",
            "CMP r0 r1 r2",
            "TRP #0"
        ]
        memory,lines, slines, labels, error = vm.assemble(testString)
        self.assertEqual(error, '')
        memory,error = vm.emulate(memory, vm.registers)
        self.assertEqual(error, '')
        self.assertEqual(vm.registers['R0'].getInt(), 0)
        self.assertEqual(vm.registers['R1'].getInt(), 2)
        self.assertEqual(vm.registers['R2'].getInt(), 2)

    def test_cmpi(self):
        self.reset()
        testString = [
            "MAIN MOVI R1 #1",
            "CMPI R0 r1 #1",
            "TRP #0"
        ]
        memory,lines, slines, labels, error = vm.assemble(testString)
        self.assertEqual(error, '')
        memory,error = vm.emulate(memory, vm.registers)
        self.assertEqual(error, '')
        self.assertEqual(vm.registers['R0'].getInt(), 0)
        self.assertEqual(vm.registers['R1'].getInt(), 1)
        self.assertEqual(vm.registers['R2'].getInt(), 0)
        self.reset()
        testString = [
            "MAIN MOVI R1 #1",
            "CMPI R0 r1 #2",
            "TRP #0"
        ]
        memory,lines, slines, labels, error = vm.assemble(testString)
        self.assertEqual(error, '')
        memory,error = vm.emulate(memory, vm.registers)
        self.assertEqual(error, '')
        self.assertEqual(vm.registers['R0'].getInt(), -1)
        self.assertEqual(vm.registers['R1'].getInt(), 1)
        self.reset()
        testString = [
            "MAIN MOVI R1 #2",
            "CMPI R0 r1 #1",
            "TRP #0"
        ]
        memory,lines, slines, labels, error = vm.assemble(testString)
        self.assertEqual(error, '')
        memory,error = vm.emulate(memory, vm.registers)
        self.assertEqual(error, '')
        self.assertEqual(vm.registers['R0'].getInt(), 1)
        self.assertEqual(vm.registers['R1'].getInt(), 2)

    def test_alci(self):
        self.reset()
        testString = [
            "MAIN ALCI R1 #3",
            "TRP #0"
        ]
        memory,lines, slines, labels, error = vm.assemble(testString)
        self.assertEqual(error, '')
        memory,error = vm.emulate(memory, vm.registers)
        self.assertEqual(error, '')
        self.assertEqual(vm.registers['R1'].getInt(), vm.registers['sb'].getInt() + 1)
        self.assertEqual(vm.registers['hp'].getInt(), vm.registers['sb'].getInt() + 4)
        
    def test_allc(self):
        self.reset()
        testString = [
            "thing .INT #4",
            "MAIN ALLC R1 thing",
            "TRP #0"
        ]
        memory,lines, slines, labels, error = vm.assemble(testString)
        self.assertEqual(error, '')
        memory,error = vm.emulate(memory, vm.registers)
        self.assertEqual(error, '')
        self.assertEqual(vm.registers['R1'].getInt(), vm.registers['sb'].getInt() + 1)
        self.assertEqual(vm.registers['hp'].getInt(), vm.registers['sb'].getInt() + 5)

    def test_iallc(self):
        self.reset()
        testString = [
            "thing .INT #4",
            "MAIN LDA R1 thing",
            "IALLC R0 R1",
            "TRP #0"
        ]
        memory,lines, slines, labels, error = vm.assemble(testString)
        self.assertEqual(error, '')
        memory,error = vm.emulate(memory, vm.registers)
        self.assertEqual(error, '')
        self.assertEqual(vm.registers['R1'].getInt(), 0)
        self.assertEqual(vm.registers['R0'].getInt(), vm.registers['sb'].getInt() + 1)
        self.assertEqual(vm.registers['hp'].getInt(), vm.registers['sb'].getInt() + 5)

    def test_pshr(self):
        self.reset()
        testString = [
            "MAIN MOVI R1 #-1",
            "PSHR R1",
            "TRP #0"
        ]
        memory,lines, slines, labels, error = vm.assemble(testString)
        self.assertEqual(error, '')
        memory,error = vm.emulate(memory, vm.registers)
        self.assertEqual(error, '')
        self.assertEqual(vm.registers['R1'].getInt(), -1)
        self.assertEqual(vm.registers['sp'].getInt(), vm.registers['sl'].getInt() + 4)
        tVal,error = vm.readInt(memory, vm.registers['sp'].getInt()-4,error)
        self.assertEqual(error, '')
        self.assertEqual(tVal, -1)

    def test_pshb(self):
        self.reset()
        testString = [
            "MAIN MOVI R1 #4",
            "PSHB R1",
            "TRP #0"
        ]
        memory,lines, slines, labels, error = vm.assemble(testString)
        self.assertEqual(error, '')
        memory,error = vm.emulate(memory, vm.registers)
        self.assertEqual(error, '')
        self.assertEqual(vm.registers['R1'].getInt(), 4)
        self.assertEqual(vm.registers['sp'].getInt(), vm.registers['sl'].getInt() + 1)
        self.assertEqual(memory[vm.registers['sp'].getInt()-1].getInt(), 4)

    def test_popr(self):
        self.reset()
        testString = [
            "MAIN MOVI R1 #4",
            "PSHR R1",
            "POPR R2",
            "TRP #0"
        ]
        memory,lines, slines, labels, error = vm.assemble(testString)
        self.assertEqual(error, '')
        memory,error = vm.emulate(memory, vm.registers)
        self.assertEqual(error, '')
        self.assertEqual(vm.registers['R2'].getInt(), 4)
        self.assertEqual(vm.registers['sp'].getInt(), vm.registers['sl'].getInt())
        self.reset()
        testString = [
            "MAIN MOVI R1 #4",
            "PSHR R1",
            "POPR R2",
            "POPR R3",
            "TRP #0"
        ]
        memory,lines, slines, labels, error = vm.assemble(testString)
        self.assertEqual(error, '')
        memory,error = vm.emulate(memory, vm.registers)
        self.assertNotEqual(error, '')

    def test_popb(self):
        self.reset()
        testString = [
            "MAIN MOVI R1 #4",
            "PSHB R1",
            "POPB R2",
            "TRP #0"
        ]
        memory,lines, slines, labels, error = vm.assemble(testString)
        self.assertEqual(error, '')
        memory,error = vm.emulate(memory, vm.registers)
        self.assertEqual(error, '')
        self.assertEqual(vm.registers['R2'].getInt(), 4)
        self.assertEqual(vm.registers['sp'].getInt(), vm.registers['sl'].getInt())
        self.reset()
        testString = [
            "MAIN MOVI R1 #4",
            "PSHB R1",
            "POPB R2",
            "POPB R3",
            "TRP #0"
        ]
        memory,lines, slines, labels, error = vm.assemble(testString)
        self.assertEqual(error, '')
        memory,error = vm.emulate(memory, vm.registers)
        self.assertNotEqual(error, '')

    def test_call(self):
        self.reset()
        testString = [
            "thing .INT #4",
            "MAIN CALL FUN",
            "movi r0 #1",
            "FUN ADDI r1 R1 #1",
            "TRP #0"
        ]
        memory,lines, slines, labels, error = vm.assemble(testString)
        self.assertEqual(error, '')
        memory,error = vm.emulate(memory, vm.registers)
        self.assertEqual(error, '')
        self.assertEqual(vm.registers['R1'].getInt(), 1)
        self.assertEqual(vm.registers['R0'].getInt(), 0)
        retVal,error = vm.readInt(memory, vm.registers['sp'].getInt()-4,error)
        self.assertEqual(error, '')
        self.assertEqual(retVal, 4)

    def test_ret(self):
        self.reset()
        testString = [
            "thing .INT #4",
            "FUN ADDI r1 R1 #1",
            "RET",
            "movi r0 #1",
            "MAIN CALL FUN",
            "TRP #0"
        ]
        memory,lines, slines, labels, error = vm.assemble(testString)
        self.assertEqual(error, '')
        memory,error = vm.emulate(memory, vm.registers)
        self.assertEqual(error, '')
        self.assertEqual(vm.registers['R1'].getInt(), 1)
        self.assertEqual(vm.registers['R0'].getInt(), 0)
        self.assertEqual(error, '')

if __name__ == '__main__':
    t = TestEmulator()
    # t.test_trp6()
    ml = [func for func in dir(TestEmulator) if callable(getattr(TestEmulator, func)) and func.startswith('test_')]
    for func in ml:
        eval(f't.{func}()')

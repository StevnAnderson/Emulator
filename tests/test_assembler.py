import unittest, os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
import vm


class TestAssembler(unittest.TestCase):

    def test_assemble(self):
        vm.firstInstruction = [-1]
        testString = [
            ".INT #-3",
            "MAIN MOV r2 r1",
            "TRP #0"
        ]
        memory,lines, slines, labels, error = vm.assemble(testString)
        self.assertEqual(lines, testString)
        self.assertEqual(error, '')
        self.assertEqual(labels, {'MAIN': 4})


    def test_noMain(self):
        vm.firstInstruction = [-1]
        testString = [
            ".INT #0",
            " MOV r2 r1",
            "TRP #0"
        ]
        memory,lines, slines, labels, error = vm.assemble(testString)
        self.assertEqual(lines, testString)
        self.assertNotEqual(error, '')
        self.assertEqual(labels, {})

    def test_str_directive(self):
        vm.firstInstruction = [-1]
        testString = [
            ".STR \"Hello World\"",
            ".STR \"!@#$%^&*()_+-=`~[] }{\"",
            "MAIN MOV r2 r1",
            "TRP #0"
        ]
        memory,lines, slines, labels, error = vm.assemble(testString)
        self.assertEqual(lines, testString)
        self.assertEqual(error, '')
        self.assertEqual(labels, {'MAIN': 36})

    def test_byt(self):
        vm.firstInstruction = [-1]
        testString = [
            ".BYT #0",
            ".BYT 'a'",
            ".BYT",
            ".BYT '\n'",
            ".BYT '\t'",
            "MAIN MOV r2 r1",
            "TRP #0"
        ]
        memory,lines, slines, labels, error = vm.assemble(testString)
        self.assertEqual(lines, testString)
        self.assertEqual(error, '')
        vm.firstInstruction = [-1]
        testString = [
            ".BYT 'ax'",
            "MAIN MOV r2 r1",
            "TRP #0"
        ]
        memory,lines, slines, labels, error = vm.assemble(testString)
        self.assertNotEqual(error, '')

    def test_bts(self):
        vm.firstInstruction = [-1]
        testString = [
            ".BTS #0",
            "thing .BTS #3",
            "MAIN MOV r2 r1",
            "TRP #0"
        ]
        memory,lines, slines, labels, error = vm.assemble(testString)
        self.assertEqual(lines, testString)
        self.assertEqual(labels, {'thing': 0, 'MAIN': 3})
        self.assertEqual(error, '')
        vm.firstInstruction = [-1]
        testString = [
            ".BTS 'ax'",
            "MAIN MOV r2 r1",
            "TRP #0"
        ]        
        memory,lines, slines, labels, error = vm.assemble(testString)
        self.assertNotEqual(error, '')
        vm.firstInstruction = [-1]
        testString = [
            ".BTS #-3",
            "MAIN MOV r2 r1",
            "TRP #0"
        ]        
        memory,lines, slines, labels, error = vm.assemble(testString)
        self.assertNotEqual(error, '')

    def test_registers(self):
        vm.firstInstruction = [-1]
        testString = [
            "MAIN MOV r2 r1",
            "MOV r3 r4",
            "MOV r5 R6",
            "MOV r7 r8",
            "MOV r9 r10",
            "MOV r11 r12",
            "MOV r13 r14",
            "MOV r15 r0",
            "TRP #0"
        ]
        memory,lines, slines, labels, error = vm.assemble(testString)
        self.assertEqual(lines, testString)
        self.assertEqual(error, '')
        vm.firstInstruction = [-1]
        testString = [
            "MAIN MOV sl r1",
            "TRP #0"
        ]
        memory,lines, slines, labels, error = vm.assemble(testString)
        self.assertNotEqual(error, '')
        vm.firstInstruction = [-1]
        testString = [
            "MAIN MOV sb r1",
        ]
        memory,lines, slines, labels, error = vm.assemble(testString)
        self.assertNotEqual(error, '')
        vm.firstInstruction = [-1]
        testString = [
            "MAIN MOV sp r1",
            "TRP #0"
        ]
        memory,lines, slines, labels, error = vm.assemble(testString)
        self.assertNotEqual(error, '')
        vm.firstInstruction = [-1]
        testString = [
            "MAIN MOV fp r1",
            "TRP #0"
        ]
        memory,lines, slines, labels, error = vm.assemble(testString)
        self.assertNotEqual(error, '')
        vm.firstInstruction = [-1]
        testString = [
            "MAIN MOV hp r1",
            "TRP #0"
        ]
        memory,lines, slines, labels, error = vm.assemble(testString)
        self.assertNotEqual(error, '')

    def test_jmp(self):
        vm.firstInstruction = [-1]
        testString = [
            "MAIN MOV r2 r1",
            "JMP end",
            "end TRP #0"
        ]
        memory,lines, slines, labels, error = vm.assemble(testString)
        self.assertEqual(lines, testString)
        self.assertEqual(error, '')
        self.assertEqual(labels, {'MAIN': 0, 'end': 16})

    def test_jmr(self):
        vm.firstInstruction = [-1]
        testString = [
            "MAIN ADDI r1 r0 #4",
            "JMR r0",
            "MOV r0 r1",
            "end TRP #0"
        ]
        memory,lines, slines, labels, error = vm.assemble(testString)
        self.assertEqual(lines, testString)
        self.assertEqual(error, '')
        # self.assertEqual(labels, {'MAIN': 1, 'end': 12})

    def test_bnz(self):
        vm.firstInstruction = [-1]
        testString = [
            "MAIN ADDI r1 r0 #4",
            "BNZ r0 end",
            "MOV r0 r1",
            "end TRP #0"
        ]
        memory,lines, slines, labels, error = vm.assemble(testString)
        self.assertEqual(lines, testString)
        self.assertEqual(error, '')

    def test_bgt(self):
        vm.firstInstruction = [-1]
        testString = [
            "MAIN ADDI r1 r0 #4",
            "BGT r0 end",
            "MOV r0 r1",
            "end TRP #0"
        ]
        memory,lines, slines, labels, error = vm.assemble(testString)
        self.assertEqual(lines, testString)
        self.assertEqual(error, '')

    def test_blt(self):
        vm.firstInstruction = [-1]
        testString = [
            "MAIN ADDI r1 r0 #-4",
            "BLT r0 end",
            "MOV r0 r1",
            "end TRP #0"
        ]
        memory,lines, slines, labels, error = vm.assemble(testString)
        self.assertEqual(lines, testString)
        self.assertEqual(error, '')

    def test_brz(self):
        vm.firstInstruction = [-1]
        testString = [
            "MAIN ADDI r1 r1 #4",
            "BRZ r0 end",
            "MOV r1 r2",
            "end TRP #0"
        ]
        memory,lines, slines, labels, error = vm.assemble(testString)
        self.assertEqual(lines, testString)
        self.assertEqual(error, '')

    def test_mov(self):
        vm.firstInstruction = [-1]
        testString = [
            "MAIN ADDI r1 r0 #2",
            "MOV r2 r1",
            "TRP #0"
        ]
        memory,lines, slines, labels, error = vm.assemble(testString)
        self.assertEqual(lines, testString)
        self.assertEqual(error, '')

    def test_lda(self):
        vm.firstInstruction = [-1]
        testString = [
            "MAIN LDA r2 end",
            "end TRP #0"
        ]
        memory,lines, slines, labels, error = vm.assemble(testString)
        self.assertEqual(lines, testString)
        self.assertEqual(error, '')

    def test_str_instruction(self):
        vm.firstInstruction = [-1]
        testString = [
            "one .INT #2",
            "MAIN ADDI r2 r3 #1",
            "STR r2 one",
            "TRP #0"
        ]
        memory,lines, slines, labels, error = vm.assemble(testString)
        self.assertEqual(lines, testString)
        self.assertEqual(error, '')

    def test_ldr(self):
        vm.firstInstruction = [-1]
        testString = [
            "one .INT #1",
            "MAIN LDR r2 one",
            "TRP #0"
        ]
        memory,lines, slines, labels, error = vm.assemble(testString)
        self.assertEqual(lines, testString)
        self.assertEqual(error, '')

    def test_stb(self):
        vm.firstInstruction = [-1]
        testString = [
            "one .INT #1",
            "MAIN STB r2 one",
            "TRP #0"
        ]
        memory,lines, slines, labels, error = vm.assemble(testString)
        self.assertEqual(lines, testString)
        self.assertEqual(error, '')

    def test_ldb(self):
        vm.firstInstruction = [-1]
        testString = [
            "one .INT #1",
            "MAIN LDB r2 one",
            "TRP #0"
        ]
        memory,lines, slines, labels, error = vm.assemble(testString)
        self.assertEqual(lines, testString)
        self.assertEqual(error, '')
    
    def test_add(self):
        vm.firstInstruction = [-1]
        testString = [
            "MAIN ADDI r2 r3 #1",
            'ADDI r1 r1 #1',
            "ADD r0 r2 r1",
            "TRP #0"
        ]
        memory,lines, slines, labels, error = vm.assemble(testString)
        self.assertEqual(lines, testString)
        self.assertEqual(error, '')
        vm.firstInstruction = [-1]
        testString = [
            "MAIN ADDI r2 r3 #1",
            'ADDI r1 r2 #1',
            "ADD r3 r2 r1",
            "TRP #0"
        ]
        memory,lines, slines, labels, error = vm.assemble(testString)
        self.assertEqual(lines, testString)
        self.assertEqual(error, '')

    def test_addi(self):
        vm.firstInstruction = [-1]
        testString = [
            "MAIN ADDI r2 r3 #1",
            "TRP #0"
        ]
        memory,lines, slines, labels, error = vm.assemble(testString)
        self.assertEqual(lines, testString)
        self.assertEqual(error, '')

    def test_sub(self):
        vm.firstInstruction = [-1]
        testString = [
            "MAIN ADDI r2 r3 #1",
            "SUB r2 r2 r0",
            "TRP #0"
        ]
        memory,lines, slines, labels, error = vm.assemble(testString)
        self.assertEqual(lines, testString)
        self.assertEqual(error, '')

    def test_mul(self):
        vm.firstInstruction = [-1]
        testString = [
            "MAIN ADDI r1 r2 #3",
            "MUL r2 r2 r2",
            "TRP #0"
        ]
        memory,lines, slines, labels, error = vm.assemble(testString)
        self.assertEqual(error, '')
        self.assertEqual(lines, testString)

    def test_div(self):
        vm.firstInstruction = [-1]
        testString = [
            "MAIN ADDI r2 r1 #6",
            "ADDI r1 r2 #3",
            "DIV r0  r2 r1",
            "TRP #0"
        ]
        memory,lines, slines, labels, error = vm.assemble(testString)
        self.assertEqual(lines, testString)
        self.assertEqual(error, '')

    def test_and(self):
        vm.firstInstruction = [-1]
        testString = [
            "MAIN ADDI r2 r3 #5",
            "ADDI r1 r2 #7",
            "AND r0 r2 r1",
            "TRP #0"
        ]
        memory,lines, slines, labels, error = vm.assemble(testString)
        self.assertEqual(lines, testString)
        self.assertEqual(error, '')
        
    def test_or(self):
        vm.firstInstruction = [-1]
        testString = [
            "MAIN ADDI r1 r2 #5",
            "ADDI r1 r1 #7",
            "OR r2 r1 r0",
            "TRP #0"
        ]
        memory,lines, slines, labels, error = vm.assemble(testString)
        self.assertEqual(lines, testString)
        self.assertEqual(error, '')

    def test_cmp(self):
        vm.firstInstruction = [-1]
        testString = [
            "MAIN ADDI r1 r1 #1",
            "ADDI r1 r2 #2",
            "CMP r1 r2 r0",
            "TRP #0"
        ]
        memory,lines, slines, labels, error = vm.assemble(testString)
        self.assertEqual(lines, testString)
        self.assertEqual(error, '')

    def test_trp(self):
        vm.firstInstruction = [-1]
        testString = [
            "WRITER .STR #24",
            "MAIN TRP #2",
            "TRP #1",
            "TRP #4",
            "TRP #3",
            "SUB R3 R3 r3",
            "LDR R3 WRITER",
            "TRP #6",
            "TRP #5",
            "TRP #0"
        ]
        memory,lines, slines, labels, error = vm.assemble(testString)
        self.assertEqual(lines, testString)
        self.assertEqual(error, '')

    def test_istr(self):
        vm.firstInstruction = [-1]
        testString = [
            "WRITER .INT #24",
            "MAIN LDA R2 WRITER",
            "ADDI r1 R1 #1",
            "ISTR R1 R2",
            "TRP #0"
        ]
        memory,lines, slines, labels, error = vm.assemble(testString)
        self.assertEqual(lines, testString)
        self.assertEqual(error, '')

    def test_ildr(self):
        vm.firstInstruction = [-1]
        testString = [
            "WRITER .INT #24",
            "MAIN LDA R2 WRITER",
            "ADDI r1 R1 #1",
            "ILDR R1 R2",
            "TRP #0"
        ]
        memory,lines, slines, labels, error = vm.assemble(testString)
        self.assertEqual(lines, testString)
        self.assertEqual(error, '')

    def test_istb(self):
        vm.firstInstruction = [-1]
        testString = [
            "WRITER .BYT",
            "MAIN LDA R2 WRITER",
            "ADDI r1 R1 #1",
            "ISTB R1 R2",
            "TRP #0"
        ]
        memory,lines, slines, labels, error = vm.assemble(testString)
        self.assertEqual(lines, testString)
        self.assertEqual(error, '')

    def test_ildb(self):
        vm.firstInstruction = [-1]
        testString = [
            "WRITER .BYT #1",
            "MAIN LDA R2 WRITER",
            "ILDB R1 R2",
            "TRP #0"
        ]
        memory,lines, slines, labels, error = vm.assemble(testString)
        self.assertEqual(lines, testString)
        self.assertEqual(error, '')

    def test_movi(self):
        vm.firstInstruction = [-1]
        testString = [
            "MAIN MOVI R1 #1",
            "TRP #0"
        ]
        memory,lines, slines, labels, error = vm.assemble(testString)
        self.assertEqual(lines, testString)
        self.assertEqual(error, '')    

    def test_cmpi(self):
        vm.firstInstruction = [-1]
        testString = [
            "MAIN MOVI R1 #1",
            "CMPI R1 r2 #1",
            "TRP #0"
        ]        
        memory,lines, slines, labels, error = vm.assemble(testString)
        self.assertEqual(lines, testString)
        self.assertEqual(error, '')

    def test_muli(self):
        vm.firstInstruction = [-1]
        testString = [
            "MAIN MOVI R1 #2",
            "MULI R1 r0 #3",
            "TRP #0"
        ]
        memory,lines, slines, labels, error = vm.assemble(testString)
        self.assertEqual(lines, testString)
        self.assertEqual(error, '')

    def test_divi(self):
        vm.firstInstruction = [-1]
        testString = [
            "MAIN MOVI R1 #6",
            "DIVI R1 r0 #3",
            "TRP #0"
        ]
        memory,lines, slines, labels, error = vm.assemble(testString)
        self.assertEqual(lines, testString)
        self.assertEqual(error, '')

    def test_alci(self):
        vm.firstInstruction = [-1]
        testString = [
            "MAIN ALCI R1 #3",
            "TRP #0"
        ]
        memory,lines, slines, labels, error = vm.assemble(testString)
        self.assertEqual(lines, testString)
        self.assertEqual(error, '')

    def test_allc(self):
        vm.firstInstruction = [-1]
        testString = [
            "goto .INT #35",
            "MAIN ALLC R1 goto",
            "TRP #0"
        ]
        memory,lines, slines, labels, error = vm.assemble(testString)
        self.assertEqual(lines, testString)
        self.assertEqual(error, '')

    def test_iallc(self):
        vm.firstInstruction = [-1]
        testString = [
            "goto .INT #35",
            "MAIN LDA R2 goto",
            "IALLC R1 R2",
            "TRP #0"
        ]
        memory,lines, slines, labels, error = vm.assemble(testString)
        self.assertEqual(lines, testString)
        self.assertEqual(error, '')
    
    def test_sdiv(self):
        vm.firstInstruction = [-1]
        testString = [
            "MAIN MOVI R1 #6",
            "ADDI r1 R2 #3",
            "SDIV R1 R2 r0",
            "TRP #0"
        ]
        memory,lines, slines, labels, error = vm.assemble(testString)
        self.assertEqual(lines, testString)
        self.assertEqual(error, '')

    def test_pshr(self):
        vm.firstInstruction = [-1]
        testString = [
            "MAIN PSHR R1",
            "TRP #0"
        ]
        memory,lines, slines, labels, error = vm.assemble(testString)
        self.assertEqual(lines, testString)
        self.assertEqual(error, '')

    def test_pshb(self):
        vm.firstInstruction = [-1]
        testString = [
            "MAIN PSHB R1",
            "TRP #0"
        ]
        memory,lines, slines, labels, error = vm.assemble(testString)
        self.assertEqual(lines, testString)
        self.assertEqual(error, '')
    
    def test_popr(self):
        vm.firstInstruction = [-1]
        testString = [
            "MAIN POPR R1",
            "TRP #0"
        ]
        memory,lines, slines, labels, error = vm.assemble(testString)
        self.assertEqual(lines, testString)
        self.assertEqual(error, '')

    def test_popb(self):
        vm.firstInstruction = [-1]
        testString = [
            "MAIN POPB R1",
            "TRP #0"
        ]
        memory,lines, slines, labels, error = vm.assemble(testString)
        self.assertEqual(lines, testString)
        self.assertEqual(error, '')

    def test_call(self):
        vm.firstInstruction = [-1]
        testString = [
            "MAIN CALL FUN",
            "FUN ADDI r1 R1 #1",
            "TRP #0"
        ]
        memory,lines, slines, labels, error = vm.assemble(testString)
        self.assertEqual(lines, testString)
        self.assertEqual(error, '')

    def test_ret(self):
        vm.firstInstruction = [-1]
        testString = [
            "MAIN CALL FUN",
            "TRP #0",
            "FUN ADDI r1 R1 #1",
            "RET"
        ]
        memory,lines, slines, labels, error = vm.assemble(testString)
        self.assertEqual(lines, testString)
        self.assertEqual(error, '')

    def test_int_mem(self):
        vm.firstInstruction = [-1]
        testString = [
            ".INT #0",
            ".INT #1",
            ".INT #-2",
            "MAIN MOV r2 r1",
            "TRP #0"
        ]
        memory,_, _, _, error = vm.assemble(testString)
        self.assertEqual(int(memory[0].value,2), 0)
        self.assertEqual(int(memory[7].value,2), 1)
        self.assertEqual(memory[11].value, '11111110')
        self.assertEqual(error, '')
        vm.firstInstruction = [-1]
        testString = [
            ".INT #-3",
            "MAIN MOV r2 r1",
            "TRP #0"
        ]
        memory,_, _, _, error = vm.assemble(testString)
        self.assertEqual(memory[0].getInt(), -1)
        self.assertEqual(memory[1].getInt(), -1)
        self.assertEqual(memory[2].getInt(), -1)
        self.assertEqual(memory[3].getInt(), -3)
        self.assertEqual(error, '') 
    
    def test_byt_mem(self):
        vm.firstInstruction = [-1]
        testString = [
            ".BYT",
            ".BYT #3",
            ".BYT 'a'",
            ".BYT '\n'",
            "MAIN MOV r2 r1",
            "TRP #0"
        ]
        memory,_, _, _, error = vm.assemble(testString)
        self.assertEqual(int(memory[0].value,2), 0)
        self.assertEqual(int(memory[1].value,2), 3)
        self.assertEqual(int(memory[2].value,2), 97)
        self.assertEqual(int(memory[3].value,2), 10)
        self.assertEqual(error, '')

    def test_bts_mem(self):
        vm.firstInstruction = [-1]
        testString = [
            ".BTS #3",
            "one .BTS #3",
            "MAIN MOV r2 r1",
            "TRP #0"
        ]
        memory,_, _, _, error = vm.assemble(testString)
        self.assertEqual(int(memory[0].value,2), 0)
        self.assertEqual(int(memory[1].value,2), 0)
        self.assertEqual(int(memory[2].value,2), 0)
        self.assertEqual(int(memory[3].value,2), 0)
        self.assertEqual(error, '')
        vm.firstInstruction = [-1]
        testString = [
            'one .BTS "a"',
            "MAIN MOV r2 r1",
            "TRP #0"
        ]
        memory,_, _, _, error = vm.assemble(testString)
        self.assertNotEqual(error,'')

    def test_str_mem(self):
        vm.firstInstruction = [-1]
        testString = [
            ' first .STR "First"',
            ".STR \"hello\"",
            "MAIN MOV r2 r1",
            "TRP #0"
        ]
        memory,_, _, _, error = vm.assemble(testString)
        self.assertEqual(int(memory[0].value,2), 5)
        self.assertEqual(int(memory[1].value,2), 70)
        self.assertEqual(int(memory[2].value,2), 105)
        self.assertEqual(int(memory[3].value,2), 114)
        self.assertEqual(int(memory[4].value,2), 115)
    
    def test_jmp_mem(self):
        vm.firstInstruction = [-1]
        testString = [
            "MAIN JMP end",
            "end TRP #0"
        ]
        memory,_, _, _, error = vm.assemble(testString)
        self.assertEqual(error, '')
        self.assertEqual(memory[0].getInt(), 1)
        self.assertEqual(memory[1].getInt(), 0)
        self.assertEqual(memory[2].getInt(), 0)
        self.assertEqual(memory[3].getInt(), 0)
        self.assertEqual(memory[4].getInt(), 0)
        self.assertEqual(memory[5].getInt(), 0)
        self.assertEqual(memory[6].getInt(), 0)
        self.assertEqual(memory[7].getInt(), 8)
        # self.assertEqual(memory[8].getInt(), 21)
    
    def test_jmr_mem(self):
        vm.firstInstruction = [-1]
        testString = [
            "MAIN JMR r3",
            "MOV r0 r1",
            "TRP #0"
        ]
        memory,_, _, _, error = vm.assemble(testString)
        self.assertEqual(error, '')
        self.assertEqual(memory[0].getInt(), 2)
        self.assertEqual(memory[1].getInt(), 3)
        self.assertEqual(memory[2].getInt(), 0)
        self.assertEqual(memory[3].getInt(), 0)
        self.assertEqual(memory[4].getInt(), 0)
        self.assertEqual(memory[5].getInt(), 0)
        self.assertEqual(memory[6].getInt(), 0)
        self.assertEqual(memory[7].getInt(), 0)

    def test_bnz_mem(self):
        vm.firstInstruction = [-1]
        testString = [
            "MAIN BNZ r3 end",
            "MOV r0 r1",
            "end TRP #0"
        ]
        memory,_, _, _, error = vm.assemble(testString)
        self.assertEqual(error, '')
        self.assertEqual(memory[0].getInt(), 3)
        self.assertEqual(memory[1].getInt(), 3)
        self.assertEqual(memory[2].getInt(), 0)
        self.assertEqual(memory[3].getInt(), 0)
        self.assertEqual(memory[4].getInt(), 0)
        self.assertEqual(memory[5].getInt(), 0)
        self.assertEqual(memory[6].getInt(), 0)
        self.assertEqual(memory[7].getInt(), 16)

    def test_bgt_mem(self):
        vm.firstInstruction = [-1]
        testString = [
            "MAIN BGT r3 end",
            "MOV r0 r1",
            "end TRP #0"
        ]
        memory,_, _, _, error = vm.assemble(testString)
        self.assertEqual(error, '')
        self.assertEqual(memory[0].getInt(), 4)
        self.assertEqual(memory[1].getInt(), 3)
        self.assertEqual(memory[2].getInt(), 0)
        self.assertEqual(memory[3].getInt(), 0)
        self.assertEqual(memory[4].getInt(), 0)
        self.assertEqual(memory[5].getInt(), 0)
        self.assertEqual(memory[6].getInt(), 0)
        self.assertEqual(memory[7].getInt(), 16)

    def test_blt_mem(self):
        vm.firstInstruction = [-1]
        testString = [
            "MAIN BLT r3 end",
            "MOV r0 r1",
            "end TRP #0"
        ]
        memory,_, _, _, error = vm.assemble(testString)
        self.assertEqual(error, '')
        self.assertEqual(memory[0].getInt(), 5)
        self.assertEqual(memory[1].getInt(), 3)
        self.assertEqual(memory[2].getInt(), 0)
        self.assertEqual(memory[3].getInt(), 0)
        self.assertEqual(memory[4].getInt(), 0)
        self.assertEqual(memory[5].getInt(), 0)
        self.assertEqual(memory[6].getInt(), 0)
        self.assertEqual(memory[7].getInt(), 16)

    def test_brz_mem(self):
        vm.firstInstruction = [-1]
        testString = [
            "MAIN BRZ r3 end",
            "MOV r0 r1",
            "end TRP #0"
        ]
        memory,_, _, _, error = vm.assemble(testString)
        self.assertEqual(error, '')
        self.assertEqual(memory[0].getInt(), 6)
        self.assertEqual(memory[1].getInt(), 3)
        self.assertEqual(memory[2].getInt(), 0)
        self.assertEqual(memory[3].getInt(), 0)
        self.assertEqual(memory[4].getInt(), 0)
        self.assertEqual(memory[5].getInt(), 0)
        self.assertEqual(memory[6].getInt(), 0)
        self.assertEqual(memory[7].getInt(), 16)
    
    def test_mov_mem(self):
        vm.firstInstruction = [-1]
        testString = [
            "MAIN MOV r0 r1",
            "TRP #0"
        ]
        memory,_, _, _, error = vm.assemble(testString)
        self.assertEqual(error, '')
        self.assertEqual(memory[0].getInt(), 7)
        self.assertEqual(memory[1].getInt(), 0)
        self.assertEqual(memory[2].getInt(), 1)
        self.assertEqual(memory[3].getInt(), 0)
        self.assertEqual(memory[4].getInt(), 0)
        self.assertEqual(memory[5].getInt(), 0)
        self.assertEqual(memory[6].getInt(), 0)
        self.assertEqual(memory[7].getInt(), 0)

    def test_movi_mem(self):
        vm.firstInstruction = [-1]
        testString = [
            "MAIN MOVI r1 #2",
            "TRP #0"
        ]
        memory,_, _, _, error = vm.assemble(testString)
        self.assertEqual(error, '')
        self.assertEqual(memory[0].getInt(), 8)
        self.assertEqual(memory[1].getInt(), 1)
        self.assertEqual(memory[2].getInt(), 0)
        self.assertEqual(memory[3].getInt(), 0)
        self.assertEqual(memory[4].getInt(), 0)
        self.assertEqual(memory[5].getInt(), 0)
        self.assertEqual(memory[6].getInt(), 0)
        self.assertEqual(memory[7].getInt(), 2)

    def test_lda_mem(self):
        vm.firstInstruction = [-1]
        testString = [
            "MAIN LDA r2 end",
            "end TRP #0"
        ]
        memory,_, _, _, error = vm.assemble(testString)
        self.assertEqual(error, '')
        self.assertEqual(memory[0].getInt(), 9)
        self.assertEqual(memory[1].getInt(), 2)
        self.assertEqual(memory[2].getInt(), 0)
        self.assertEqual(memory[3].getInt(), 0)
        self.assertEqual(memory[4].getInt(), 0)
        self.assertEqual(memory[5].getInt(), 0)
        self.assertEqual(memory[6].getInt(), 0)
        self.assertEqual(memory[7].getInt(), 8)

    def test_str_mem(self):
        vm.firstInstruction = [-1]
        testString = [
            'strlock .INT #0',
            'addi r2 r2 #1',
            'MAIN STR r2 strlock',
            'TRP #0'
        ]
        memory,_, _, _, error = vm.assemble(testString)
        self.assertEqual(error, '')
        self.assertEqual(memory[12].getInt(), 10)
        self.assertEqual(memory[13].getInt(), 2)
        self.assertEqual(memory[14].getInt(), 0)
        self.assertEqual(memory[15].getInt(), 0)
        self.assertEqual(memory[16].getInt(), 0)
        self.assertEqual(memory[17].getInt(), 0)
        self.assertEqual(memory[18].getInt(), 0)
        self.assertEqual(memory[19].getInt(), 0)

    def test_ldr_mem(self):
        vm.firstInstruction = [-1]
        testString = [
            '.INT #0',
            'ldrlock .INT #12',
            'MAIN LDR r2 ldrlock',
            'TRP #0'
        ]
        memory,_, _, _, error = vm.assemble(testString)
        self.assertEqual(error, '')
        self.assertEqual(memory[8].getInt(), 11)
        self.assertEqual(memory[9].getInt(), 2)
        self.assertEqual(memory[10].getInt(), 0)
        self.assertEqual(memory[11].getInt(), 0)
        self.assertEqual(memory[12].getInt(), 0)
        self.assertEqual(memory[13].getInt(), 0)
        self.assertEqual(memory[14].getInt(), 0)
        self.assertEqual(memory[15].getInt(), 4)

    def test_stb_mem(self):
        vm.firstInstruction = [-1]
        testString = [
            '.INT #0',
            'one .INT #1',
            'MAIN STB r2 one',
            'TRP #0'
        ]
        memory,_, _, _, error = vm.assemble(testString)
        self.assertEqual(error, '')
        self.assertEqual(memory[8].getInt(), 12)
        self.assertEqual(memory[9].getInt(), 2)
        self.assertEqual(memory[10].getInt(), 0)
        self.assertEqual(memory[11].getInt(), 0)
        self.assertEqual(memory[12].getInt(), 0)
        self.assertEqual(memory[13].getInt(), 0)
        self.assertEqual(memory[14].getInt(), 0)
        self.assertEqual(memory[15].getInt(), 4)

    def test_ldb_mem(self):
        vm.firstInstruction = [-1]
        testString = [
            '.INT #0',
            'one .INT #1',
            'MAIN LDB r2 one',
            'TRP #0'
        ]
        memory,_, _, _, error = vm.assemble(testString)
        self.assertEqual(error, '')
        self.assertEqual(memory[8].getInt(), 13)
        self.assertEqual(memory[9].getInt(), 2)
        self.assertEqual(memory[10].getInt(), 0)
        self.assertEqual(memory[11].getInt(), 0)
        self.assertEqual(memory[12].getInt(), 0)
        self.assertEqual(memory[13].getInt(), 0)
        self.assertEqual(memory[14].getInt(), 0)
        self.assertEqual(memory[15].getInt(), 4)

    def test_istr_mem(self):
        vm.firstInstruction = [-1]
        testString = [
            'MAIN ISTR r2 r1',
            'TRP #0'
        ]
        memory,_, _, _, error = vm.assemble(testString)
        self.assertEqual(error, '')
        self.assertEqual(memory[0].getInt(), 14)
        self.assertEqual(memory[1].getInt(), 2)
        self.assertEqual(memory[2].getInt(), 1)
        self.assertEqual(memory[3].getInt(), 0)
        self.assertEqual(memory[4].getInt(), 0)
        self.assertEqual(memory[5].getInt(), 0)
        self.assertEqual(memory[6].getInt(), 0)
        self.assertEqual(memory[7].getInt(), 0)

    def test_ildr_mem(self):
        vm.firstInstruction = [-1]
        testString = [
            'MAIN ILDR r2 r1',
            'TRP #0'
        ]
        memory,_, _, _, error = vm.assemble(testString)
        self.assertEqual(error, '')
        self.assertEqual(memory[0].getInt(), 15)
        self.assertEqual(memory[1].getInt(), 2)
        self.assertEqual(memory[2].getInt(), 1)
        self.assertEqual(memory[3].getInt(), 0)
        self.assertEqual(memory[4].getInt(), 0)
        self.assertEqual(memory[5].getInt(), 0)
        self.assertEqual(memory[6].getInt(), 0)

    def test_istb_mem(self):
        vm.firstInstruction = [-1]
        testString = [
            'MAIN ISTB r2 r1',
            'TRP #0'
        ]
        memory,_, _, _, error = vm.assemble(testString)
        self.assertEqual(error, '')
        self.assertEqual(memory[0].getInt(), 16)
        self.assertEqual(memory[1].getInt(), 2)
        self.assertEqual(memory[2].getInt(), 1)
        self.assertEqual(memory[3].getInt(), 0)
        self.assertEqual(memory[4].getInt(), 0)
        self.assertEqual(memory[5].getInt(), 0)
        self.assertEqual(memory[6].getInt(), 0)

    def test_ildb_mem(self):
        vm.firstInstruction = [-1]
        testString = [
            'MAIN ILDB r2 r1',
            'TRP #0'
        ]
        memory,_, _, _, error = vm.assemble(testString)
        self.assertEqual(error, '')
        self.assertEqual(memory[0].getInt(), 17)
        self.assertEqual(memory[1].getInt(), 2)
        self.assertEqual(memory[2].getInt(), 1)
        self.assertEqual(memory[3].getInt(), 0)
        self.assertEqual(memory[4].getInt(), 0)
        self.assertEqual(memory[5].getInt(), 0)
        self.assertEqual(memory[6].getInt(), 0)

    def test_add_mem(self):
        vm.firstInstruction = [-1]
        testString = [
            'MAIN ADD r2 r1 r3',
            'TRP #0'
        ]
        memory,_, _, _, error = vm.assemble(testString)
        self.assertEqual(error, '')
        self.assertEqual(memory[0].getInt(), 18)
        self.assertEqual(memory[1].getInt(), 2)
        self.assertEqual(memory[2].getInt(), 1)
        self.assertEqual(memory[3].getInt(), 3)
        self.assertEqual(memory[4].getInt(), 0)
        self.assertEqual(memory[5].getInt(), 0)
        self.assertEqual(memory[6].getInt(), 0)
    
    def test_addi_mem(self):
        vm.firstInstruction = [-1]
        testString = [
            'MAIN ADDI r2 r1 #1',
            'TRP #0'
        ]
        memory,_, _, _, error = vm.assemble(testString)
        self.assertEqual(error, '')
        self.assertEqual(memory[0].getInt(), 19)
        self.assertEqual(memory[1].getInt(), 2)
        self.assertEqual(memory[2].getInt(), 1)
        self.assertEqual(memory[3].getInt(), 0)
        self.assertEqual(memory[4].getInt(), 0)
        self.assertEqual(memory[5].getInt(), 0)
        self.assertEqual(memory[6].getInt(), 0)
        self.assertEqual(memory[7].getInt(), 1)

    def test_sub_mem(self):
        vm.firstInstruction = [-1]
        testString = [
            'MAIN SUB r2 r1 r3',
            'TRP #0'
        ]
        memory,_, _, _, error = vm.assemble(testString)
        self.assertEqual(error, '')
        self.assertEqual(memory[0].getInt(), 20)
        self.assertEqual(memory[1].getInt(), 2)
        self.assertEqual(memory[2].getInt(), 1)
        self.assertEqual(memory[3].getInt(), 3)
        self.assertEqual(memory[4].getInt(), 0)
        self.assertEqual(memory[5].getInt(), 0)
        self.assertEqual(memory[6].getInt(), 0)

    def test_subi_mem(self):
        vm.firstInstruction = [-1]
        testString = [
            'MAIN SUBI r2 r1 #1',
            'TRP #0'
        ]
        memory,_, _, _, error = vm.assemble(testString)
        self.assertEqual(error, '')
        self.assertEqual(memory[0].getInt(), 21)
        self.assertEqual(memory[1].getInt(), 2)
        self.assertEqual(memory[2].getInt(), 1)
        self.assertEqual(memory[3].getInt(), 0)
        self.assertEqual(memory[4].getInt(), 0)
        self.assertEqual(memory[5].getInt(), 0)
        self.assertEqual(memory[6].getInt(), 0)
        self.assertEqual(memory[7].getInt(), 1)

    def test_mul_mem(self):
        vm.firstInstruction = [-1]
        testString = [
            'MAIN MUL r2 r1 r3',
            'TRP #0'
        ]
        memory,_, _, _, error = vm.assemble(testString)
        self.assertEqual(error, '')
        self.assertEqual(memory[0].getInt(), 22)
        self.assertEqual(memory[1].getInt(), 2)
        self.assertEqual(memory[2].getInt(), 1)
        self.assertEqual(memory[3].getInt(), 3)
        self.assertEqual(memory[4].getInt(), 0)
        self.assertEqual(memory[5].getInt(), 0)
        self.assertEqual(memory[6].getInt(), 0)
        self.assertEqual(memory[7].getInt(), 0)

    def test_muli_mem(self):
        vm.firstInstruction = [-1]
        testString = [
            'MAIN MULI r2 r1 #1',
            'TRP #0'
        ]
        memory,_, _, _, error = vm.assemble(testString)
        self.assertEqual(error, '')
        self.assertEqual(memory[0].getInt(), 23)
        self.assertEqual(memory[1].getInt(), 2)
        self.assertEqual(memory[2].getInt(), 1)
        self.assertEqual(memory[3].getInt(), 0)
        self.assertEqual(memory[4].getInt(), 0)
        self.assertEqual(memory[5].getInt(), 0)
        self.assertEqual(memory[6].getInt(), 0)
        self.assertEqual(memory[7].getInt(), 1)
        
    def test_div_mem(self):
        vm.firstInstruction = [-1]
        testString = [
            'MAIN DIV r2 r1 r3',
            'TRP #0'
        ]
        memory,_, _, _, error = vm.assemble(testString)
        self.assertEqual(error, '')
        self.assertEqual(memory[0].getInt(), 24)
        self.assertEqual(memory[1].getInt(), 2)
        self.assertEqual(memory[2].getInt(), 1)
        self.assertEqual(memory[3].getInt(), 3)
        self.assertEqual(memory[4].getInt(), 0)
        self.assertEqual(memory[5].getInt(), 0)
        self.assertEqual(memory[6].getInt(), 0)

    def test_sdiv_mem(self):
        vm.firstInstruction = [-1]
        testString = [
            'MAIN SDIV r2 r1 r3',
            'TRP #0'
        ]
        memory,_, _, _, error = vm.assemble(testString)
        self.assertEqual(error, '')
        self.assertEqual(memory[0].getInt(), 25)
        self.assertEqual(memory[1].getInt(), 2)
        self.assertEqual(memory[2].getInt(), 1)
        self.assertEqual(memory[3].getInt(), 3)
        self.assertEqual(memory[4].getInt(), 0)
        self.assertEqual(memory[5].getInt(), 0)
        self.assertEqual(memory[6].getInt(), 0)

    def test_divi_mem(self):
        vm.firstInstruction = [-1]
        testString = [
            'MAIN DIVI r2 r1 #1',
            'TRP #0'
        ]
        memory,_, _, _, error = vm.assemble(testString)
        self.assertEqual(error, '')
        self.assertEqual(memory[0].getInt(), 26)
        self.assertEqual(memory[1].getInt(), 2)
        self.assertEqual(memory[2].getInt(), 1)
        self.assertEqual(memory[3].getInt(), 0)
        self.assertEqual(memory[4].getInt(), 0)
        self.assertEqual(memory[5].getInt(), 0)
        self.assertEqual(memory[6].getInt(), 0)
        self.assertEqual(memory[7].getInt(), 1)

    def test_and_mem(self):
        vm.firstInstruction = [-1]
        testString = [
            'MAIN AND r2 r1 r3',
            'TRP #0'
        ]
        memory,_, _, _, error = vm.assemble(testString)
        self.assertEqual(error, '')
        self.assertEqual(memory[0].getInt(), 27)
        self.assertEqual(memory[1].getInt(), 2)
        self.assertEqual(memory[2].getInt(), 1)
        self.assertEqual(memory[3].getInt(), 3)
        self.assertEqual(memory[4].getInt(), 0)
        self.assertEqual(memory[5].getInt(), 0)
        self.assertEqual(memory[6].getInt(), 0)
        self.assertEqual(memory[7].getInt(), 0)

    def test_or_mem(self):
        vm.firstInstruction = [-1]
        testString = [
            'MAIN OR r2 r1 r3',
            'TRP #0'
        ]
        memory,_, _, _, error = vm.assemble(testString)
        self.assertEqual(error, '')
        self.assertEqual(memory[0].getInt(), 28)
        self.assertEqual(memory[1].getInt(), 2)
        self.assertEqual(memory[2].getInt(), 1)
        self.assertEqual(memory[3].getInt(), 3)
        self.assertEqual(memory[4].getInt(), 0)
        self.assertEqual(memory[5].getInt(), 0)
        self.assertEqual(memory[6].getInt(), 0)
        self.assertEqual(memory[7].getInt(), 0)

    def test_cmp_mem(self):
        vm.firstInstruction = [-1]
        testString = [
            'MAIN CMP r2 r1 r3',
            'TRP #0'
        ]
        memory,_, _, _, error = vm.assemble(testString)
        self.assertEqual(error, '')
        self.assertEqual(memory[0].getInt(), 29)
        self.assertEqual(memory[1].getInt(), 2)
        self.assertEqual(memory[2].getInt(), 1)
        self.assertEqual(memory[3].getInt(), 3)
        self.assertEqual(memory[4].getInt(), 0)
        self.assertEqual(memory[5].getInt(), 0)
        self.assertEqual(memory[6].getInt(), 0)
        self.assertEqual(memory[7].getInt(), 0)

    def test_cmpi_mem(self):
        vm.firstInstruction = [-1]
        testString = [
            'MAIN CMPI r2 r1 #1',
            'TRP #0'
        ]
        memory,_, _, _, error = vm.assemble(testString)
        self.assertEqual(error, '')
        self.assertEqual(memory[0].getInt(), 30)
        self.assertEqual(memory[1].getInt(), 2)
        self.assertEqual(memory[2].getInt(), 1)
        self.assertEqual(memory[3].getInt(), 0)
        self.assertEqual(memory[4].getInt(), 0)
        self.assertEqual(memory[5].getInt(), 0)
        self.assertEqual(memory[6].getInt(), 0)
        self.assertEqual(memory[7].getInt(), 1)

    def test_trp_mem(self):
        vm.firstInstruction = [-1]
        testString = [
            'MAIN TRP #1',
            'TRP #0'
        ]
        memory,_, _, _, error = vm.assemble(testString)
        self.assertEqual(error, '')
        self.assertEqual(memory[0].getInt(), 31)
        self.assertEqual(memory[1].getInt(), 0)
        self.assertEqual(memory[2].getInt(), 0)
        self.assertEqual(memory[3].getInt(), 0)
        self.assertEqual(memory[4].getInt(), 0)
        self.assertEqual(memory[5].getInt(), 0)
        self.assertEqual(memory[6].getInt(), 0)
        self.assertEqual(memory[7].getInt(), 1)

    def test_alci_mem(self):
        vm.firstInstruction = [-1]
        testString = [
            'MAIN ALCI r1 #3',
            'TRP #0'
        ]
        memory,_, _, _, error = vm.assemble(testString)
        self.assertEqual(error, '')
        self.assertEqual(memory[0].getInt(), 32)
        self.assertEqual(memory[1].getInt(), 1)
        self.assertEqual(memory[2].getInt(), 0)
        self.assertEqual(memory[3].getInt(), 0)
        self.assertEqual(memory[4].getInt(), 0)
        self.assertEqual(memory[5].getInt(), 0)
        self.assertEqual(memory[6].getInt(), 0)
        self.assertEqual(memory[7].getInt(), 3)
        vm.firstInstruction = [-1]
        testString = [
            'bad .INT #1',
            'MAIN ALCI r1 bad',
            'TRP #0'
        ]
        memory,_, _, _, error = vm.assemble(testString)
        self.assertNotEqual(error, '')

    def test_allc_mem(self):
        vm.firstInstruction = [-1]
        testString = [
            '.INT #2',
            'old .INT #3',
            'MAIN ALLC r1 old',
            'TRP #0'
        ]
        memory,_, _, _, error = vm.assemble(testString)
        self.assertEqual(error, '')
        self.assertEqual(memory[8].getInt(), 33)
        self.assertEqual(memory[9].getInt(), 1)
        self.assertEqual(memory[10].getInt(), 0)
        self.assertEqual(memory[11].getInt(), 0)
        self.assertEqual(memory[12].getInt(), 0)
        self.assertEqual(memory[13].getInt(), 0)
        self.assertEqual(memory[14].getInt(), 0)
        self.assertEqual(memory[15].getInt(), 4)
        vm.firstInstruction = [-1]
        testString = [
            'bad .INT #1',
            'MAIN ALLC r1 #5',
            'TRP #0'
        ]
        memory,_, _, _, error = vm.assemble(testString)
        self.assertNotEqual(error, '')

    def test_iallc_mem(self):
        vm.firstInstruction = [-1]
        testString = [
            'MAIN IALLC r1 r3',
            'TRP #0'
        ]
        memory,_, _, _, error = vm.assemble(testString)
        self.assertEqual(error, '')
        self.assertEqual(memory[0].getInt(), 34)
        self.assertEqual(memory[1].getInt(), 1)
        self.assertEqual(memory[2].getInt(), 3)
        self.assertEqual(memory[3].getInt(), 0)
        self.assertEqual(memory[4].getInt(), 0)
        self.assertEqual(memory[5].getInt(), 0)
        self.assertEqual(memory[6].getInt(), 0)
        self.assertEqual(memory[7].getInt(), 0)
        vm.firstInstruction = [-1]
        testString = [
            'bad .INT #1',
            'MAIN IALLC r1 #5',
            'TRP #0'
        ]
        memory,_, _, _, error = vm.assemble(testString)
        self.assertNotEqual(error, '')

    def test_pshr_mem(self):
        vm.firstInstruction = [-1]
        testString = [
            'MAIN PSHR r1',
            'TRP #0'
        ]
        memory,_, _, _, error = vm.assemble(testString)
        self.assertEqual(error, '')
        self.assertEqual(memory[0].getInt(), 35)
        self.assertEqual(memory[1].getInt(), 1)
        self.assertEqual(memory[2].getInt(), 0)
        self.assertEqual(memory[3].getInt(), 0)
        self.assertEqual(memory[4].getInt(), 0)
        self.assertEqual(memory[5].getInt(), 0)
        self.assertEqual(memory[6].getInt(), 0)
        self.assertEqual(memory[7].getInt(), 0)
        vm.firstInstruction = [-1]
        testString = [
            'MAIN PSHR #3 r2',
            'TRP #0'
        ]
        memory,_, _, _, error = vm.assemble(testString)
        self.assertNotEqual(error, '')

    def test_pshb_mem(self):
        vm.firstInstruction = [-1]
        testString = [
            'MAIN PSHB r1',
            'TRP #0'
        ]
        memory,_, _, _, error = vm.assemble(testString)
        self.assertEqual(error, '')
        self.assertEqual(memory[0].getInt(), 36)
        self.assertEqual(memory[1].getInt(), 1)
        self.assertEqual(memory[2].getInt(), 0)
        self.assertEqual(memory[3].getInt(), 0)
        self.assertEqual(memory[4].getInt(), 0)
        self.assertEqual(memory[5].getInt(), 0)
        self.assertEqual(memory[6].getInt(), 0)
        self.assertEqual(memory[7].getInt(), 0)
        vm.firstInstruction = [-1]
        testString = [
            'MAIN PSHB #3 r2',
            'TRP #0'
        ]
        memory,_, _, _, error = vm.assemble(testString)
        self.assertNotEqual(error, '')

    def test_popr_mem(self):
        vm.firstInstruction = [-1]
        testString = [
            'MAIN POPR r1',
            'TRP #0'
        ]
        memory,_, _, _, error = vm.assemble(testString)
        self.assertEqual(error, '')
        self.assertEqual(memory[0].getInt(), 37)
        self.assertEqual(memory[1].getInt(), 1)
        self.assertEqual(memory[2].getInt(), 0)
        self.assertEqual(memory[3].getInt(), 0)
        self.assertEqual(memory[4].getInt(), 0)
        self.assertEqual(memory[5].getInt(), 0)
        self.assertEqual(memory[6].getInt(), 0)
        self.assertEqual(memory[7].getInt(), 0)
        vm.firstInstruction = [-1]
        testString = [
            'MAIN POPR #3 r2',
            'TRP #0'
        ]
        memory,_, _, _, error = vm.assemble(testString)
        self.assertNotEqual(error, '')

    def test_popb_mem(self):
        vm.firstInstruction = [-1]
        testString = [
            'MAIN POPB r1',
            'TRP #0'
        ]
        memory,_, _, _, error = vm.assemble(testString)
        self.assertEqual(error, '')
        self.assertEqual(memory[0].getInt(), 38)
        self.assertEqual(memory[1].getInt(), 1)
        self.assertEqual(memory[2].getInt(), 0)
        self.assertEqual(memory[3].getInt(), 0)
        self.assertEqual(memory[4].getInt(), 0)
        self.assertEqual(memory[5].getInt(), 0)
        self.assertEqual(memory[6].getInt(), 0)
        self.assertEqual(memory[7].getInt(), 0)
        vm.firstInstruction = [-1]
        testString = [
            'MAIN POPB #3 r2',
            'TRP #0'
        ]
        memory,_, _, _, error = vm.assemble(testString)
        self.assertNotEqual(error, '')

    def test_call(self):
        vm.firstInstruction = [-1]
        testString = [
            'MAIN CALL end',
            'end TRP #0'
        ]
        memory,_, _, _, error = vm.assemble(testString)
        self.assertEqual(error, '')
        self.assertEqual(memory[0].getInt(), 39)
        self.assertEqual(memory[1].getInt(), 0)
        self.assertEqual(memory[2].getInt(), 0)
        self.assertEqual(memory[3].getInt(), 0)
        self.assertEqual(memory[4].getInt(), 0)
        self.assertEqual(memory[5].getInt(), 0)
        self.assertEqual(memory[6].getInt(), 0)
        self.assertEqual(memory[7].getInt(), 8)
        vm.firstInstruction = [-1]
        testString = [
            'MAIN CALL r2',
            'TRP #0'
        ]
        memory,_, _, _, error = vm.assemble(testString)
        self.assertNotEqual(error, '')

    def test_ret_mem(self):
        vm.firstInstruction = [-1]
        testString = [
            'MAIN RET',
            'TRP #0'
        ]
        memory,_, _, _, error = vm.assemble(testString)
        self.assertEqual(error, '')
        self.assertEqual(memory[0].getInt(), 40)
        self.assertEqual(memory[1].getInt(), 0)
        self.assertEqual(memory[2].getInt(), 0)
        self.assertEqual(memory[3].getInt(), 0)
        self.assertEqual(memory[4].getInt(), 0)
        self.assertEqual(memory[5].getInt(), 0)
        self.assertEqual(memory[6].getInt(), 0)
        self.assertEqual(memory[7].getInt(), 0)
        vm.firstInstruction = [-1]
        testString = [
            'MAIN RET r2',
            'TRP #0'
        ]

if __name__ == '__main__':
    t = TestAssembler()
    t.test_addi_mem()
    # ml = [func for func in dir(TestAssembler) if callable(getattr(TestAssembler, func)) and func.startswith('test_')]
    # for func in ml:
    #     eval(f't.{func}()')

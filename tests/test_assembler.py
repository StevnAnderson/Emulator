import unittest
try:
    import src.assembler as assembler
except:
    import assembler as assembler


class TestAssembler(unittest.TestCase):

    def test_assemble(self):
        assembler.firstInstruction = [-1]
        testString = [
            ".INT #-3",
            "MAIN MOV r2 r1",
            "TRP #0"
        ]
        lines, slines, labels, error = assembler.assemble(testString)
        self.assertEqual(lines, testString)
        self.assertEqual(error, '')
        self.assertEqual(labels, {'MAIN': 2})


    def test_noMain(self):
        assembler.firstInstruction = [-1]
        testString = [
            ".INT #0",
            " MOV r2 r1",
            "TRP #0"
        ]
        lines, slines, labels, error = assembler.assemble(testString)
        self.assertEqual(lines, testString)
        self.assertNotEqual(error, '')
        self.assertEqual(labels, {})

    def test_str_directive(self):
        assembler.firstInstruction = [-1]
        testString = [
            ".STR \"Hello World\"",
            ".STR \"!@#$%^&*()_+-=`~[] }{\"",
            "MAIN MOV r2 r1",
            "TRP #0"
        ]
        lines, slines, labels, error = assembler.assemble(testString)
        self.assertEqual(lines, testString)
        self.assertEqual(error, '')
        self.assertEqual(labels, {'MAIN': 3})

    def test_byt(self):
        assembler.firstInstruction = [-1]
        testString = [
            ".BYT #0",
            ".BYT 'a'",
            ".BYT",
            ".BYT '\n'",
            ".BYT '\t'",
            "MAIN MOV r2 r1",
            "TRP #0"
        ]
        lines, slines, labels, error = assembler.assemble(testString)
        self.assertEqual(lines, testString)
        self.assertEqual(error, '')
        assembler.firstInstruction = [-1]
        testString = [
            ".BYT 'ax'",
            "MAIN MOV r2 r1",
            "TRP #0"
        ]
        lines, slines, labels, error = assembler.assemble(testString)
        self.assertEqual(lines, testString)
        self.assertNotEqual(error, '')
        self.assertEqual(labels, {'MAIN': 2})

    def test_bts(self):
        assembler.firstInstruction = [-1]
        testString = [
            ".BTS #0",
            "thing .BTS #3",
            "MAIN MOV r2 r1",
            "TRP #0"
        ]
        lines, slines, labels, error = assembler.assemble(testString)
        self.assertEqual(lines, testString)
        self.assertEqual(labels, {'THING': 2, 'MAIN': 3})
        self.assertEqual(error, '')
        assembler.firstInstruction = [-1]
        testString = [
            ".BTS 'ax'",
            "MAIN MOV r2 r1",
            "TRP #0"
        ]        
        lines, slines, labels, error = assembler.assemble(testString)
        self.assertNotEqual(error, '')
        assembler.firstInstruction = [-1]
        testString = [
            ".BTS #-3",
            "MAIN MOV r2 r1",
            "TRP #0"
        ]        
        lines, slines, labels, error = assembler.assemble(testString)
        self.assertNotEqual(error, '')

    def test_registers(self):
        assembler.firstInstruction = [-1]
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
        lines, slines, labels, error = assembler.assemble(testString)
        self.assertEqual(lines, testString)
        self.assertEqual(error, '')
        assembler.firstInstruction = [-1]
        testString = [
            "MAIN MOV sl r1",
            "TRP #0"
        ]
        lines, slines, labels, error = assembler.assemble(testString)
        self.assertNotEqual(error, '')
        assembler.firstInstruction = [-1]
        testString = [
            "MAIN MOV sb r1",
        ]
        lines, slines, labels, error = assembler.assemble(testString)
        self.assertNotEqual(error, '')
        assembler.firstInstruction = [-1]
        testString = [
            "MAIN MOV sp r1",
            "TRP #0"
        ]
        lines, slines, labels, error = assembler.assemble(testString)
        self.assertNotEqual(error, '')
        assembler.firstInstruction = [-1]
        testString = [
            "MAIN MOV fp r1",
            "TRP #0"
        ]
        lines, slines, labels, error = assembler.assemble(testString)
        self.assertNotEqual(error, '')
        assembler.firstInstruction = [-1]
        testString = [
            "MAIN MOV hp r1",
            "TRP #0"
        ]
        lines, slines, labels, error = assembler.assemble(testString)
        self.assertNotEqual(error, '')

    def test_jmp(self):
        assembler.firstInstruction = [-1]
        testString = [
            "MAIN MOV r2 r1",
            "JMP end",
            "end TRP #0"
        ]
        lines, slines, labels, error = assembler.assemble(testString)
        self.assertEqual(lines, testString)
        self.assertEqual(error, '')
        self.assertEqual(labels, {'MAIN': 1, 'END': 3})

    def test_jmr(self):
        assembler.firstInstruction = [-1]
        testString = [
            "MAIN ADDI r0 #4",
            "JMR end",
            "MOV r0 r1",
            "end TRP #0"
        ]
        lines, slines, labels, error = assembler.assemble(testString)
        self.assertEqual(lines, testString)
        self.assertEqual(error, '')
        self.assertEqual(labels, {'MAIN': 1, 'END': 4})

    def test_bnz(self):
        assembler.firstInstruction = [-1]
        testString = [
            "MAIN ADDI r0 #4",
            "BNZ r0 end",
            "MOV r0 r1",
            "end TRP #0"
        ]
        lines, slines, labels, error = assembler.assemble(testString)
        self.assertEqual(lines, testString)
        self.assertEqual(error, '')

    def test_bgt(self):
        assembler.firstInstruction = [-1]
        testString = [
            "MAIN ADDI r0 #4",
            "BGT r0 end",
            "MOV r0 r1",
            "end TRP #0"
        ]
        lines, slines, labels, error = assembler.assemble(testString)
        self.assertEqual(lines, testString)
        self.assertEqual(error, '')

    def test_blt(self):
        assembler.firstInstruction = [-1]
        testString = [
            "MAIN ADDI r0 #-4",
            "BLT r0 end",
            "MOV r0 r1",
            "end TRP #0"
        ]
        lines, slines, labels, error = assembler.assemble(testString)
        self.assertEqual(lines, testString)
        self.assertEqual(error, '')

    def test_brz(self):
        assembler.firstInstruction = [-1]
        testString = [
            "MAIN ADDI r1 #4",
            "BRZ r0 end",
            "MOV r1 r2",
            "end TRP #0"
        ]
        lines, slines, labels, error = assembler.assemble(testString)
        self.assertEqual(lines, testString)
        self.assertEqual(error, '')

    def test_mov(self):
        assembler.firstInstruction = [-1]
        testString = [
            "MAIN addi r0 #2",
            "MOV r2 r1",
            "TRP #0"
        ]
        lines, slines, labels, error = assembler.assemble(testString)
        self.assertEqual(lines, testString)
        self.assertEqual(error, '')

    def test_lda(self):
        assembler.firstInstruction = [-1]
        testString = [
            "MAIN LDA r2 end",
            "end TRP #0"
        ]
        lines, slines, labels, error = assembler.assemble(testString)
        self.assertEqual(lines, testString)
        self.assertEqual(error, '')

    def test_str_instruction(self):
        assembler.firstInstruction = [-1]
        testString = [
            "one .INT #2",
            "MAIN addi r2 #1",
            "STR r2 one",
            "TRP #0"
        ]
        lines, slines, labels, error = assembler.assemble(testString)
        self.assertEqual(lines, testString)
        self.assertEqual(error, '')

    def test_ldr(self):
        assembler.firstInstruction = [-1]
        testString = [
            "one .INT #1",
            "MAIN LDR r2 one",
            "TRP #0"
        ]
        lines, slines, labels, error = assembler.assemble(testString)
        self.assertEqual(lines, testString)
        self.assertEqual(error, '')

    def test_stb(self):
        assembler.firstInstruction = [-1]
        testString = [
            "one .INT #1",
            "MAIN STB r2 one",
            "TRP #0"
        ]
        lines, slines, labels, error = assembler.assemble(testString)
        self.assertEqual(lines, testString)
        self.assertEqual(error, '')

    def test_ldb(self):
        assembler.firstInstruction = [-1]
        testString = [
            "one .INT #1",
            "MAIN LDB r2 one",
            "TRP #0"
        ]
        lines, slines, labels, error = assembler.assemble(testString)
        self.assertEqual(lines, testString)
        self.assertEqual(error, '')
    
    def test_add(self):
        assembler.firstInstruction = [-1]
        testString = [
            "MAIN ADDI r2 #1",
            'ADDI r1 #1',
            "ADD r2 r1",
            "TRP #0"
        ]
        lines, slines, labels, error = assembler.assemble(testString)
        self.assertEqual(lines, testString)
        self.assertEqual(error, '')

    def test_addi(self):
        assembler.firstInstruction = [-1]
        testString = [
            "MAIN ADDI r2 #1",
            "TRP #0"
        ]
        lines, slines, labels, error = assembler.assemble(testString)
        self.assertEqual(lines, testString)
        self.assertEqual(error, '')

    def test_sub(self):
        assembler.firstInstruction = [-1]
        testString = [
            "MAIN ADDI r2 #1",
            "SUB r2 r2",
            "TRP #0"
        ]
        lines, slines, labels, error = assembler.assemble(testString)
        self.assertEqual(lines, testString)
        self.assertEqual(error, '')

    def test_mul(self):
        assembler.firstInstruction = [-1]
        testString = [
            "MAIN ADDI r2 #3",
            "MUL r2 r2",
            "TRP #0"
        ]
        lines, slines, labels, error = assembler.assemble(testString)
        self.assertEqual(lines, testString)
        self.assertEqual(error, '')

    def test_div(self):
        assembler.firstInstruction = [-1]
        testString = [
            "MAIN ADDI r2 #6",
            "ADDI r1 #3",
            "DIV r2 r1",
            "TRP #0"
        ]
        lines, slines, labels, error = assembler.assemble(testString)
        self.assertEqual(lines, testString)
        self.assertEqual(error, '')

    def test_and(self):
        assembler.firstInstruction = [-1]
        testString = [
            "MAIN ADDI r2 #5",
            "ADDI r1 #7",
            "AND r2 r1",
            "TRP #0"
        ]
        lines, slines, labels, error = assembler.assemble(testString)
        self.assertEqual(lines, testString)
        self.assertEqual(error, '')
        
    def test_or(self):
        assembler.firstInstruction = [-1]
        testString = [
            "MAIN ADDI r2 #5",
            "ADDI r1 #7",
            "OR r2 r1",
            "TRP #0"
        ]
        lines, slines, labels, error = assembler.assemble(testString)
        self.assertEqual(lines, testString)
        self.assertEqual(error, '')

    def test_cmp(self):
        assembler.firstInstruction = [-1]
        testString = [
            "MAIN ADDI r1 #1",
            "ADDI r2 #2",
            "CMP r1 r2",
            "TRP #0"
        ]
        lines, slines, labels, error = assembler.assemble(testString)
        self.assertEqual(lines, testString)
        self.assertEqual(error, '')

    def test_trp(self):
        assembler.firstInstruction = [-1]
        testString = [
            "WRITER .STR #24",
            "MAIN TRP #2",
            "TRP #1",
            "TRP #4",
            "TRP #3",
            "SUB R3 R3",
            "LDR R3 WRITER",
            "TRP #6",
            "TRP #5",
            "TRP #0"
        ]
        lines, slines, labels, error = assembler.assemble(testString)
        self.assertEqual(lines, testString)
        self.assertEqual(error, '')

    def test_istr(self):
        assembler.firstInstruction = [-1]
        testString = [
            "WRITER .INT #24",
            "MAIN LDA R2 WRITER",
            "ADDI R1 #1",
            "ISTR R1 R2",
            "TRP #0"
        ]
        lines, slines, labels, error = assembler.assemble(testString)
        self.assertEqual(lines, testString)
        self.assertEqual(error, '')

    def test_ildr(self):
        assembler.firstInstruction = [-1]
        testString = [
            "WRITER .INT #24",
            "MAIN LDA R2 WRITER",
            "ADDI R1 #1",
            "ILDR R1 R2",
            "TRP #0"
        ]
        lines, slines, labels, error = assembler.assemble(testString)
        self.assertEqual(lines, testString)
        self.assertEqual(error, '')

    def test_istb(self):
        assembler.firstInstruction = [-1]
        testString = [
            "WRITER .BYT",
            "MAIN LDA R2 WRITER",
            "ADDI R1 #1",
            "ISTB R1 R2",
            "TRP #0"
        ]
        lines, slines, labels, error = assembler.assemble(testString)
        self.assertEqual(lines, testString)
        self.assertEqual(error, '')

    def test_ildb(self):
        assembler.firstInstruction = [-1]
        testString = [
            "WRITER .BYT #1",
            "MAIN LDA R2 WRITER",
            "ILDB R1 R2",
            "TRP #0"
        ]
        lines, slines, labels, error = assembler.assemble(testString)
        self.assertEqual(lines, testString)
        self.assertEqual(error, '')

    def test_movi(self):
        assembler.firstInstruction = [-1]
        testString = [
            "MAIN MOVI R1 #1",
            "TRP #0"
        ]
        lines, slines, labels, error = assembler.assemble(testString)
        self.assertEqual(lines, testString)
        self.assertEqual(error, '')    

    def test_cmpi(self):
        assembler.firstInstruction = [-1]
        testString = [
            "MAIN MOVI R1 #1",
            "CMPI R1 #1",
            "TRP #0"
        ]        
        lines, slines, labels, error = assembler.assemble(testString)
        self.assertEqual(lines, testString)
        self.assertEqual(error, '')

    def test_muli(self):
        assembler.firstInstruction = [-1]
        testString = [
            "MAIN MOVI R1 #2",
            "MULI R1 #3",
            "TRP #0"
        ]
        lines, slines, labels, error = assembler.assemble(testString)
        self.assertEqual(lines, testString)
        self.assertEqual(error, '')

    def test_divi(self):
        assembler.firstInstruction = [-1]
        testString = [
            "MAIN MOVI R1 #6",
            "DIVI R1 #3",
            "TRP #0"
        ]
        lines, slines, labels, error = assembler.assemble(testString)
        self.assertEqual(lines, testString)
        self.assertEqual(error, '')

    def test_alci(self):
        assembler.firstInstruction = [-1]
        testString = [
            "MAIN ALCI R1 #3",
            "TRP #0"
        ]
        lines, slines, labels, error = assembler.assemble(testString)
        self.assertEqual(lines, testString)
        self.assertEqual(error, '')

    def test_allc(self):
        assembler.firstInstruction = [-1]
        testString = [
            "goto .INT #35",
            "MAIN ALLC R1 goto",
            "TRP #0"
        ]
        lines, slines, labels, error = assembler.assemble(testString)
        self.assertEqual(lines, testString)
        self.assertEqual(error, '')

    def test_iallc(self):
        assembler.firstInstruction = [-1]
        testString = [
            "goto .INT #35",
            "MAIN LDA R2 goto",
            "IALLC R1 R2",
            "TRP #0"
        ]
        lines, slines, labels, error = assembler.assemble(testString)
        self.assertEqual(lines, testString)
        self.assertEqual(error, '')
    
    def test_sdiv(self):
        assembler.firstInstruction = [-1]
        testString = [
            "MAIN MOVI R1 #6",
            "ADDI R2 #3"
            "SDIV R1 R2",
            "TRP #0"
        ]
        lines, slines, labels, error = assembler.assemble(testString)
        self.assertEqual(lines, testString)
        self.assertEqual(error, '')

    def test_pshr(self):
        assembler.firstInstruction = [-1]
        testString = [
            "MAIN PSHR R1",
            "TRP #0"
        ]
        lines, slines, labels, error = assembler.assemble(testString)
        self.assertEqual(lines, testString)
        self.assertEqual(error, '')

    def test_pshb(self):
        assembler.firstInstruction = [-1]
        testString = [
            "MAIN PSHB R1",
            "TRP #0"
        ]
        lines, slines, labels, error = assembler.assemble(testString)
        self.assertEqual(lines, testString)
        self.assertEqual(error, '')
    
    def test_popr(self):
        assembler.firstInstruction = [-1]
        testString = [
            "MAIN POPR R1",
            "TRP #0"
        ]
        lines, slines, labels, error = assembler.assemble(testString)
        self.assertEqual(lines, testString)
        self.assertEqual(error, '')

    def test_popb(self):
        assembler.firstInstruction = [-1]
        testString = [
            "MAIN POPB R1",
            "TRP #0"
        ]
        lines, slines, labels, error = assembler.assemble(testString)
        self.assertEqual(lines, testString)
        self.assertEqual(error, '')

    def test_call(self):
        assembler.firstInstruction = [-1]
        testString = [
            "MAIN CALL FUN",
            "FUN ADDI R1 #1",
            "TRP #0"
        ]
        lines, slines, labels, error = assembler.assemble(testString)
        self.assertEqual(lines, testString)
        self.assertEqual(error, '')

    def test_ret(self):
        assembler.firstInstruction = [-1]
        testString = [
            "MAIN CALL FUN",
            "TRP #0",
            "FUN ADDI R1 #1",
            "RET"
        ]
        lines, slines, labels, error = assembler.assemble(testString)
        self.assertEqual(lines, testString)
        self.assertEqual(error, '')

if __name__ == '__main__':
    t = TestAssembler()
    t.test_assemble()
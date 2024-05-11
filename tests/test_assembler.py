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
        lines, labels, error = assembler.assemble(testString)
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
        lines, labels, error = assembler.assemble(testString)
        self.assertEqual(lines, testString)
        self.assertNotEqual(error, '')
        self.assertEqual(labels, {})

    def test_str(self):
        assembler.firstInstruction = [-1]
        testString = [
            ".STR \"Hello World\"",
            "MAIN MOV r2 r1",
            "TRP #0"
        ]
        lines, labels, error = assembler.assemble(testString)
        self.assertEqual(lines, testString)
        self.assertEqual(error, '')
        self.assertEqual(labels, {'MAIN': 2})

if __name__ == '__main__':
    t = TestAssembler()
    t.test_str()
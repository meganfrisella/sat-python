import unittest
from solver import (
    Literal,
    Clause,
    readInput,
    pureLiteralElim
)
"""
noClause => UNSAT
oneClause => SAT
twoClause1 => formula becomes empty
twoClause2 => formula doesn't change
manyClause1 => vars 2 and 3 removed
manyClause2 => SAT
"""
def getInputs(filename):
    varset, clauseSet = readInput(filename)
    varAssignment = dict.fromkeys(varset, -1)
    return varAssignment, clauseSet

class PureLitElimTests(unittest.TestCase):
    
    def test_no_clause(self):
        varAssignment, formula = getInputs("test_files/noClause.txt")
        self.assertEqual(pureLiteralElim(varAssignment, formula), (varAssignment, formula))
    
    def test_one_clause(self):
        varAssignment, formula = getInputs("test_files/oneClause.txt")
        new_varAssignment = varAssignment.copy()
        new_varAssignment['1'] = True
        self.assertEqual(pureLiteralElim(varAssignment, formula), (new_varAssignment, []))
    
    def test_two_clause1(self):
        varAssignment, formula = getInputs("test_files/twoClause1.txt")
        new_varAssignment = varAssignment.copy()
        new_varAssignment['1'] = False
        self.assertEqual(pureLiteralElim(varAssignment, formula), (new_varAssignment, []))
    
    def test_two_clause2(self):
        varAssignment, formula = getInputs("test_files/twoClause2.txt")
        self.assertEqual(pureLiteralElim(varAssignment, formula), (varAssignment, formula))
    
    def test_two_many_clause1(self):
        varAssignment, formula = getInputs("test_files/manyClause1.txt")
        new_varAssignment = varAssignment.copy()
        new_varAssignment['2'] = False
        new_varAssignment['3'] = True
        _, new_formula = getInputs("test_files/manyClause1output.txt")
        self.assertEqual(pureLiteralElim(varAssignment, formula), (new_varAssignment, new_formula))

if __name__ == '__main__':
    unittest.main()

import unittest
from solver import (
    Literal,
    Clause,
    readInput,
    unitClauseElim
)

"""
noClause => UNSAT
oneClause => SAT
twoClause1 => SAT
twoClause2 => UNSAT
manyClause1 => new formula doesn't contain var 1 or 2
manyClause3 => formula doesn't change
"""

def getInputs(filename):
    varset, clauseSet = readInput(filename)
    varAssignment = dict.fromkeys(varset, -1)
    return varAssignment, clauseSet

class UnitClauseElimTests(unittest.TestCase):

    def test_no_clause(self):
        varAssignment, formula = getInputs("test_files/noClause.txt")
        self.assertEqual(unitClauseElim(varAssignment, formula), (varAssignment, formula))

    def test_one_clause(self):
        varAssignment, formula = getInputs("test_files/oneClause.txt")
        new_varAssignment = varAssignment.copy()
        new_varAssignment['1'] = 1
        self.assertEqual(unitClauseElim(varAssignment, formula), (new_varAssignment, []))

    def test_two_clause1(self):
        varAssignment, formula = getInputs("test_files/twoClause1.txt")
        new_varAssignment = varAssignment.copy()
        new_varAssignment['1'] = 0
        self.assertEqual(unitClauseElim(varAssignment, formula), (new_varAssignment, []))

    def test_two_clause2(self):
        varAssignment, formula = getInputs("test_files/twoClause2.txt")
        new_varAssignment = varAssignment.copy()
        new_varAssignment['1'] = 0
        new_formula = [Clause(id=1, literalSet=[])]
        self.assertEqual(unitClauseElim(varAssignment, formula), (new_varAssignment, new_formula))

    def test_two_many_clause1(self):
        varAssignment, formula = getInputs("test_files/manyClause1.txt")
        new_varAssignment = varAssignment.copy()
        new_varAssignment['1'] = 1
        new_varAssignment['2'] = 0
        new_formula = [Clause(id=2, literalSet=[3])]
        self.assertEqual(unitClauseElim(varAssignment, formula), (new_varAssignment, new_formula))

if __name__ == '__main__':
    unittest.main()

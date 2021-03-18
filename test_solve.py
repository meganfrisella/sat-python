import unittest
from solver import (
    Literal,
    Clause,
    solve,
    readInput
)

def evaluate(filename):
    '''
    Evaluates the given assignments and tests in python boolean logic
    if it is satisfiable. If it's not satisfiable returns false.
    '''
    varset, clauseSet = readInput(filename)
    varAssignment = dict.fromkeys(varset, -1)
    varAssignment = solve(varAssignment, clauseSet)

    # NOTE: there isn't really a way to check this
    if varAssignment is None:
        return False

    for c in clauseSet:
        clause = []
        for lit in c.literalSet:
            if lit.sign:
                clause.append(bool(varAssignment[lit.name]))
            else:
                clause.append(not(bool(varAssignment[lit.name])))
        if not(any(clause)):
            return False

    return True

class SolveTests(unittest.TestCase):

    def test_some_none_clause_False(self):
        self.assertFalse(evaluate("test_files/noClause.txt"))
        self.assertFalse(evaluate("test_files/twoClause2.txt"))
        self.assertFalse(evaluate("test_files/manyClauseFalse.txt"))

    def test_some_clause_True(self):
        self.assertTrue(evaluate("test_files/oneClause.txt"))
        self.assertTrue(evaluate("test_files/twoClause1.txt"))
        self.assertTrue(evaluate("test_files/twoClause3.txt"))

    def test_many_clauses(self):
        self.assertTrue(evaluate("test_files/manyClause1.txt"))
        self.assertTrue(evaluate("test_files/manyClause2.txt"))
        self.assertTrue(evaluate("test_files/manyClause3.txt"))

    def test_large_clauses(self):
        self.assertTrue(evaluate("test_files/NEGrandomComplexClause.txt"))
        self.assertTrue(evaluate("test_files/POSrandomComplexClause.txt"))
        self.assertFalse(evaluate("test_files/manyClauseFalse5.txt"))

if __name__ == '__main__':
    unittest.main()

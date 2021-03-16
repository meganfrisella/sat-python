import unittest
from solver import (
    Literal,
    Clause,
    solve,
    readInput
)
# case 0: no clauses or empty clause?

# case 1: one literal one clause formula

# case 2: one literal two clause formulas
    # sign same, sign different -> SAT, UNSAT
# case 3:
    # a, a b, -a c -> unit elim from final a

# case 4:
    #

def evaluate(filename):

    # is it sat or not
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

    def test_some_clause_True(self):
        self.assertTrue(evaluate("test_files/oneClause.txt"))
        self.assertTrue(evaluate("test_files/twoClause1.txt"))
        self.assertTrue(evaluate("test_files/twoClause3.txt"))

    def test_many_clauses(self):
        self.assertTrue(evaluate("test_files/manyClause1.txt"))
        self.assertTrue(evaluate("test_files/manyClause2.txt"))
        self.assertTrue(evaluate("test_files/manyClause3.txt"))

if __name__ == '__main__':
    unittest.main()

import unittest
from solver import (
    Literal,
    Clause,
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
class UnitClauseElimTests(unittest.TestCase):

    def test_format(self):
        # dict[Literal, int]
        in_varAssignment = {Literal(name="5", 1): -1}
        # list[Clause]
        in_formula = [Clause(id=234, literalSet=Literal(name="5", 1))]
        ##
        out_varAssignment = None
        out_formula = None
        out = (out_varAssignment, out_formula)
        ##
        self.assertEqual(unitClauseElim(in_varAssignment, in_formula), out)

if __name__ == '__main__':
    unittest.main()

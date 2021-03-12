import unittest
from solver import (
    Literal,
    Clause,
    unitClauseElim
)

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

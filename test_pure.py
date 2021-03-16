import unittest
from solver import (
    Literal,
    Clause,
    pureLiteralElim
)
"""
noClause => UNSAT
oneClause => SAT
twoClause1 => formula doesn't change
twoClause2 => formula doesn't change
manyClause1 => vars 2 and 3 removed
manyClause2 => SAT
"""
class PureLitElimTests(unittest.TestCase):

    def test_format(self):
        # dict[Literal, int]
        in_varAssignment = None
        # list[Clause]
        in_formula = None
        ##
        out_varAssignment = None
        out_formula = None
        out = (out_varAssignment, out_formula)
        ##
        self.assertEqual(pureLiteralElim(in_varAssignment, in_formula), out)

if __name__ == '__main__':
    unittest.main()

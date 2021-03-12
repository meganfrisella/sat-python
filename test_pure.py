import unittest
from solver import (
    Literal,
    Clause,
    pureLiteralElim
)

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

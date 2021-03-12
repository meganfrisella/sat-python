import unittest
from solver import (
    Literal,
    Clause,
    solve
)

class SolveTests(unittest.TestCase):

    def test_format(self):
        in_varAssignment = None
        in_formula = None
        ##
        out_varAssignment = None
        ##
        self.assertEqual(solve(in_varAssignment, in_formula), out_varAssignment)

if __name__ == '__main__':
    unittest.main()

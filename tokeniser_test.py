from ast import *
import unittest
from tokeniser import *

class TestASTEval(unittest.TestCase):

    def test_can_tokenise_single_digit_number(self):
        expr = "5"
        tokeniser = Tokeniser(expr)
        self.assertEqual(tokeniser.tokenise(), [Literal(5)])

    def test_can_tokenise_multi_digit_number(self):
        expr = "41.67"
        tokeniser = Tokeniser(expr)
        self.assertEqual(tokeniser.tokenise(), [Literal(41.67)])

    def test_can_tokenise_expression(self):
        expr = "41.2 + 67.9"
        tokeniser = Tokeniser(expr)
        self.assertEqual(tokeniser.tokenise(), [Literal(41.2), Op("+"), Literal(67.9)])

    def test_can_tokenise_diff_with_variables(self):
        expr = "diff(y, x)"
        tokeniser = Tokeniser(expr)
        expected = [
            Variable('diff'), 
            Op.LPAREN, 
            Variable('y'), 
            Op.COMMA, 
            Variable('x'), 
            Op.RPAREN
        ]
        self.assertEqual(tokeniser.tokenise(), expected)

    def test_can_tokenise_variable_with_number(self):
        expr = "x1 + 10"
        tokeniser = Tokeniser(expr)
        
        expected_tokens = [
            Variable('x1'), 
            Op.ADD, 
            Literal(10.0)
        ]
        
        self.assertEqual(tokeniser.tokenise(), expected_tokens)


if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False, verbosity=2)
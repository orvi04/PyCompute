from math import exp
import token
import unittest

from parser import *
from tokeniser import *

class TestASTEval(unittest.TestCase):

    def test_can_parse_literal(self):
        expr = [Literal(5)]
        parser = Parser(expr)
        self.assertEqual(parser.parse(), Literal(5))

    def test_can_parse_addition(self):
        expr = [Literal(9), Op('+'), Literal(10)]
        parser = Parser(expr)
        self.assertEqual(parser.parse(), Operator(Op.ADD, Literal(9), Literal(10)))

    def test_parses_with_bodmas(self):
        expr = [Literal(2), Op('+'), Literal(3), Op('*'), Literal(4)]
        parser = Parser(expr)
        self.assertEqual(parser.parse(), Operator(Op.ADD, Literal(2), Operator(Op.MULTIPLY, Literal(3), Literal(4))))

    def test_parses_with_left_association(self):
        expr = [Literal(10), Op('-'), Literal(5), Op('-'), Literal(2)]
        parser = Parser(expr)
        self.assertEqual(parser.parse(), Operator(Op.SUBTRACT, Operator(Op.SUBTRACT, Literal(10), Literal(5)), Literal(2)))

    def test_parses_with_brackets(self):
        expr = [Op.LPAREN, Literal(2), Op('+'), Literal(3), Op.RPAREN, Op('*'), Literal(4)]
        parser = Parser(expr)

        inner_expr = Operator(Op.ADD, Literal(2), Literal(3))
        expected_ast = Operator(Op.MULTIPLY, inner_expr, Literal(4))

        self.assertEqual(parser.parse(), expected_ast)

    def test_parses_exponents(self):
        expr = [Literal(4), Op.EXPONENT, Literal(2)]
        parser = Parser(expr)
        self.assertEqual(parser.parse(), expr)

    def test_can_parse_from_tokeniser(self):
        expr = "2 + 3 * 4"

        tokeniser = Tokeniser(expr)
        tokens = tokeniser.tokenise()

        parser = Parser(tokens)
        self.assertEqual(parser.parse(), Operator(Op.ADD, Literal(2), Operator(Op.MULTIPLY, Literal(3), Literal(4))))

    def test_can_parse_brackets_from_tokeniser(self):
        expr = "2 * ((6 + 4) / 10)"

        tokeniser = Tokeniser(expr)
        tokens = tokeniser.tokenise()

        parser = Parser(tokens)

        expr1 = Operator(Op.ADD, Literal(6), Literal(4))
        expr2 = Operator(Op.DIVIDE, expr1, Literal(10))
        expected_expr = Operator(Op.MULTIPLY, Literal(2), expr2)

        self.assertEqual(parser.parse(), expected_expr)

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False, verbosity=2)
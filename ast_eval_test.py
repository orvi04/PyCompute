import unittest

from ast_eval import *


class TestASTEval(unittest.TestCase):

    def test_can_make_integer_literal(self):
        expr = Literal(41)
        self.assertEqual(eval(expr), 41)

    def test_can_make_float_literal(self):
        expr = Literal(67.0)
        self.assertEqual(eval(expr), 67.0)

    def test_can_perform_ops_on_literals(self):
        num1 = Literal(21)
        num2 = Literal(7)
        expr = Operator(Op.SUBTRACT, num1, num2)
        self.assertEqual(eval(expr), 14)

    def test_can_perform_exponents(self):
        num1 = Literal(2)
        num2 = Literal(4)
        num3 = Literal(5)
        expr1 = Operator(Op.EXPONENT, num2, num1)
        expr2 = Operator(Op.EXPONENT, num3, num1)
        self.assertEqual(eval(expr1), 16)
        self.assertEqual(eval(expr2), 25)


    def test_can_perform_ops_on_expr(self):
        expr_l = Operator(Op.ADD, Literal(41), Literal(1))
        expr_r = Operator(Op.MULTIPLY, Literal(7), Literal(2))
        expr = Operator(Op.DIVIDE, expr_l, Operator(Op.ADD, expr_r, Literal(1)))
        self.assertEqual(eval(expr), 2.8)

    def test_can_eval_simple_expr_from_parser(self):
        expr1 = Operator(Op.ADD, Literal(6), Literal(4))
        expr2 = Operator(Op.DIVIDE, expr1, Literal(10))
        expected_expr = Operator(Op.MULTIPLY, Literal(2), expr2)
        self.assertEqual(eval(expected_expr), 2)


if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False, verbosity=2)
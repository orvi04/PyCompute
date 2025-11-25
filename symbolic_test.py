import unittest
from ast_eval import *
from symbolic import *

X = Variable('x')
Y = Variable('y')
L0 = Literal(0)
L1 = Literal(1)
L2 = Literal(2)
L3 = Literal(3)
L5 = Literal(5)

class TestDifferentiation(unittest.TestCase):

    def test_01_constant_rule(self):
        """d/dx(5) should be 0."""
        expr = L5
        expected = L0
        self.assertEqual(differentiate(expr, 'x'), expected)

    def test_02_variable_rule(self):
        """d/dx(x) should be 1."""
        expr = X
        expected = L1
        self.assertEqual(differentiate(expr, 'x'), expected)

    def test_03_partial_diff_rule(self):
        """d/dx(y) should be 0."""
        expr = Y
        expected = L0
        self.assertEqual(differentiate(expr, 'x'), expected)

    def test_04_sum_rule(self):
        """d/dx(x + 5) should be (d/dx(x) + d/dx(5)) -> (1 + 0)."""
        expr = Operator(Op.ADD, X, L5)
        expected = Operator(Op.ADD, L1, L0)
        self.assertEqual(differentiate(expr, 'x'), expected)

    def test_05_unary_rule(self):
        """d/dx(-x) should be -(d/dx(x)) -> -1."""
        expr = UnaryOp(Op.SUBTRACT, X)
        expected = UnaryOp(Op.SUBTRACT, L1)
        self.assertEqual(differentiate(expr, 'x'), expected)

    def test_06_power_rule(self):
        """d/dx(x^3) should be 3 * x^2 * 1."""
        expr = Operator(Op.EXPONENT, X, L3)
        # Expected AST structure: (3 * (x ^ 2)) * 1
        inner_power = Operator(Op.EXPONENT, X, L2)
        multiplier = Operator(Op.MULTIPLY, L3, inner_power)
        expected = Operator(Op.MULTIPLY, multiplier, L1)
        self.assertEqual(differentiate(expr, 'x'), expected)

    def test_07_product_rule(self):
        """d/dx(x * 5) should be (1 * 5) + (x * 0)."""
        expr = Operator(Op.MULTIPLY, X, L5)
        # Expected AST structure: ((1 * 5) + (x * 0))
        left_part = Operator(Op.MULTIPLY, L1, L5)
        right_part = Operator(Op.MULTIPLY, X, L0)
        expected = Operator(Op.ADD, left_part, right_part)
        self.assertEqual(differentiate(expr, 'x'), expected)

    def test_08_quotient_rule(self):
        """d/dx(5 / x) structure test: ((0*x) - (5*1)) / x^2."""
        expr = Operator(Op.DIVIDE, L5, X)
        # Expected Numerator: ((0 * x) - (5 * 1))
        num_left = Operator(Op.MULTIPLY, L0, X)
        num_right = Operator(Op.MULTIPLY, L5, L1)
        numerator = Operator(Op.SUBTRACT, num_left, num_right)
        
        # Expected Denominator: x^2
        denominator = Operator(Op.EXPONENT, X, L2)

        expected = Operator(Op.DIVIDE, numerator, denominator)
        self.assertEqual(differentiate(expr, 'x'), expected)

class TestSimplification(unittest.TestCase):
    """Tests the simplify function identity rules."""

    def test_10_add_identity_left(self):
        """x + 0 should be x."""
        expr = Operator(Op.ADD, X, L0)
        self.assertEqual(simplify(expr), X)
        
    def test_11_add_identity_right(self):
        """0 + x should be x."""
        expr = Operator(Op.ADD, L0, X)
        self.assertEqual(simplify(expr), X)

    def test_12_mult_identity(self):
        """x * 1 should be x."""
        expr = Operator(Op.MULTIPLY, X, L1)
        self.assertEqual(simplify(expr), X)

    def test_13_mult_zero(self):
        """x * 0 should be 0."""
        expr = Operator(Op.MULTIPLY, X, L0)
        self.assertEqual(simplify(expr), L0)

    def test_14_sub_identity(self):
        """x - 0 should be x."""
        expr = Operator(Op.SUBTRACT, X, L0)
        self.assertEqual(simplify(expr), X)
        
    def test_15_double_negation(self):
        """-(-x) should be x."""
        expr = UnaryOp(Op.SUBTRACT, UnaryOp(Op.SUBTRACT, X))
        self.assertEqual(simplify(expr), X)

    def test_16_power_identity(self):
        """x ^ 1 should be x."""
        expr = Operator(Op.EXPONENT, X, L1)
        self.assertEqual(simplify(expr), X)

    def test_17_power_zero(self):
        """x ^ 0 should be 1."""
        expr = Operator(Op.EXPONENT, X, L0)
        self.assertEqual(simplify(expr), L1)
        
    def test_18_constant_folding(self):
        """(5 * 2) + 1 should be 11.0."""
        inner = Operator(Op.MULTIPLY, L5, L2) # 10
        expr = Operator(Op.ADD, inner, L1)    # 10 + 1
        expected = Literal(11.0)
        self.assertEqual(simplify(expr), expected)

    
class TestPipeline(unittest.TestCase):
    """Tests the combination of differentiation and simplification."""

    def test_20_basic_power_rule_cleaned(self):
        """d/dx(x^2) should result in 2 * x (cleaned)."""
        expr = Operator(Op.EXPONENT, X, L2)
        
        # Derivative: (2 * x^1) * 1
        derivative_tree = differentiate(expr, 'x')
        
        # Expected Clean Tree: (2 * x)
        expected = Operator(Op.MULTIPLY, L2, X)
        self.assertEqual(simplify(derivative_tree), expected)

    def test_21_product_rule_cleaned(self):
        """d/dx(x * x) should result in 2 * x."""
        expr = Operator(Op.MULTIPLY, X, X)
        
        # Derivative: ((1*x) + (x*1))
        derivative_tree = differentiate(expr, 'x')
        
        # Expected Clean Tree: (x + x)
        expected = Operator(Op.ADD, X, X)
        self.assertEqual(simplify(derivative_tree), expected)


if __name__ == '__main__':
    # Running with high verbosity to see all test details
    unittest.main(argv=['first-arg-is-ignored'], exit=False, verbosity=2)
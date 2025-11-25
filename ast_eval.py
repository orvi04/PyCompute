from __future__ import annotations

import enum
from dataclasses import dataclass
from typing import Literal, Union

class SymbolicResultError(Exception):
    """Raised when evaluation hits a symbolic variable and cannot return a number."""
    def __init__(self, node):
        self.node = node

class Op(enum.Enum):
    ADD = '+'
    SUBTRACT = '-'
    MULTIPLY = '*'
    DIVIDE = '/'
    EXPONENT = '^'
    LPAREN = '(' 
    RPAREN = ')'
    COMMA = ','

Expr = Union['Literal', 'Operator', 'UnaryOp', 'Diff', 'Variable']

@dataclass(frozen=True)
class Variable:
    name: str
    def __repr__(self): return f"{self.name}"

@dataclass(frozen=True)
class Diff:
    expression: Expr
    var: str = 'x'

    def __repr__(self): return f"Diff({self.expression}, {self.var})"

@dataclass(frozen=True)
class UnaryOp:
    op: Op
    operand: Expr

    def __repr__(self):
        return f"{self.op.value}({self.operand})"

@dataclass(frozen=True)
class Literal:
    value: Union[int, float]

    def __repr__(self):
        return f"{self.value}"

    def __eq__(self, other):
        if isinstance(other, Literal):
            return self.value == other.value
        return self.value == other

@dataclass(frozen=True)
class Operator:
    op: Op
    left: Expr
    right: Expr

    def __repr__(self):
        return f"({self.left} {self.op.value} {self.right})"

AST_NODE_TYPES = (Literal, Operator, UnaryOp, Diff, Variable)

def eval(expression):
    if isinstance(expression, Literal):
        return expression.value

    elif isinstance(expression, Variable):
        raise SymbolicResultError(expression)

    elif isinstance(expression, UnaryOp):
        try:
            val = eval(expression.operand)
            if expression.op == Op.SUBTRACT:
                return -val
            return val
        except SymbolicResultError as e:
            raise SymbolicResultError(UnaryOp(expression.op, e.node))
    
    elif isinstance(expression, Operator):
        try:
            left_val = eval(expression.left)
        except SymbolicResultError as e:
            left_val = e.node
        try:
            right_val = eval(expression.right)
        except SymbolicResultError as e:
            right_val = e.node

        is_symbolic = isinstance(left_val, AST_NODE_TYPES) or isinstance(right_val, AST_NODE_TYPES)

        if not is_symbolic:
            if expression.op == Op.ADD:
                return left_val + right_val
            elif expression.op == Op.SUBTRACT:
                return left_val - right_val
            elif expression.op == Op.MULTIPLY:
                return left_val * right_val
            elif expression.op == Op.DIVIDE:
                if right_val == 0:
                    raise ZeroDivisionError("Cannot divide by zero.")
                return left_val / right_val
            elif expression.op == Op.EXPONENT:
                return left_val ** right_val
        else:
            new_left = left_val if isinstance(left_val, Expr) else Literal(left_val)
            new_right = right_val if isinstance(right_val, Expr) else Literal(right_val)

            raise SymbolicResultError(Operator(expression.op, new_left, new_right))
        
    elif isinstance(expression, Diff):
        from symbolic import differentiate, simplify

        derivative_tree = differentiate(expression.expression, expression.var)
        simplified_tree = simplify(derivative_tree)

        raise SymbolicResultError(simplified_tree)

    raise TypeError(f"Unknown expression type: {type(expression)}")


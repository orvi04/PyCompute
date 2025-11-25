import enum
from dataclasses import dataclass
from typing import Literal, Union

class Op(enum.Enum):
    ADD = '+'
    SUBTRACT = '-'
    MULTIPLY = '*'
    DIVIDE = '/'
    EXPONENT = '^'
    LPAREN = '(' 
    RPAREN = ')'

Expr = Union['Literal', 'Operator']

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

def eval(expression):
    if isinstance(expression, Literal):
        return expression.value
    
    elif isinstance(expression, Operator):
        left_val = eval(expression.left)
        right_val = eval(expression.right)

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
        
        raise TypeError(f"Unknown expression type: {type(expression)}")


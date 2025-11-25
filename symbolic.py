from multiprocessing import Value
from ast_eval import *

def differentiate(node: Expr, var_name: str):
        
    if isinstance(node, Literal):
        return Literal(0.0)
        
    elif isinstance(node, Variable):
        if node.name == var_name:
            return Literal(1.0)
        return Literal(0.0)


    elif isinstance(node, UnaryOp):
        du = differentiate(node.operand, var_name)
        return UnaryOp(node.op, du)

    
    if isinstance(node, Operator):
        u = node.left
        v = node.right

        du = differentiate(u, var_name)
        dv = differentiate(v, var_name)

        if node.op == Op.ADD:
            return Operator(Op.ADD, du, dv)
        if node.op == Op.SUBTRACT:
            return Operator(Op.SUBTRACT, du, dv)

        if node.op == Op.MULTIPLY:
            left = Operator(Op.MULTIPLY, du, v)
            right = Operator(Op.MULTIPLY, u, dv)
            return Operator(Op.ADD, left, right)
        if node.op == Op.DIVIDE:
            du_v = Operator(Op.MULTIPLY, du, v)
            u_v_prime = Operator(Op.MULTIPLY, u, dv)
            numerator = Operator(Op.SUBTRACT, du_v, u_v_prime)
            denominator = Operator(Op.EXPONENT, v, Literal(2.0))
            return Operator(Op.DIVIDE, numerator, denominator)

        if node.op == Op.EXPONENT:
            if isinstance(v, Literal):
                n = v
            elif isinstance(v, UnaryOp) and v.op == Op.SUBTRACT and isinstance(v.operand, Literal):
                n = Literal(-v.operand.value) 
            else:
                raise ValueError(f"Differentiation not implemented for non-constant exponent: {v}")


            new_expt_val = n.value - 1
            new_expt = Literal(new_expt_val)

            power = Operator(Op.MULTIPLY, n, Operator(Op.EXPONENT, u, new_expt))

            return Operator(Op.MULTIPLY, power, du)

    raise ValueError(f"Differentiation not implemented for operator type: {node.op}")

def simplify(node: Expr):
    
    if isinstance(node, (Literal, Variable)):
        return node

    if isinstance(node, UnaryOp):
        operand = simplify(node.operand)

        if operand == Literal(0):
            return Literal(0.0)

        if node.op == Op.SUBTRACT and isinstance(operand, UnaryOp) and operand.op == Op.SUBTRACT:
            return operand.operand

        return UnaryOp(node.op, operand)

    if isinstance(node, Operator):
        left = simplify(node.left)
        right = simplify(node.right)

        if isinstance(left, Literal) and isinstance(right, Literal):
            if node.op == Op.ADD: return Literal(left.value + right.value)
            if node.op == Op.SUBTRACT: return Literal(left.value - right.value)
            if node.op == Op.MULTIPLY: return Literal(left.value * right.value)
            if node.op == Op.EXPONENT: return Literal(left.value ** right.value)
            if node.op == Op.DIVIDE:
                if right == Literal(0.0):
                    raise ZeroDivisionError("Cannot divide by zero")
                return Literal(left.value / right.value)

        if node.op == Op.ADD:
            if right == Literal(0): return left
            if left == Literal(0): return right

        if node.op == Op.SUBTRACT:
            if right == Literal(0): return left

        if node.op == Op.MULTIPLY:
            if right == Literal(1): return left
            if left == Literal(1): return right
            if right == Literal(0): return Literal(0.0)
            if left == Literal(0): return Literal(0.0)

        if node.op == Op.EXPONENT:
            if right == Literal(1): return left
            if right == Literal(0) and not (left == Literal(0)): return Literal(1.0)
            if left == Literal(0): return Literal(0.0)

        return Operator(node.op, left, right)

    return node
        
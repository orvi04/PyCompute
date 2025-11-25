from ast_eval import *

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.current_token = self.tokens[0] if tokens else None

    def advance(self):
        self.pos += 1
        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]
        else:
            self.current_token = None

    def parse(self):
        result = self.parse_expression()

        if self.current_token is not None:
            raise ValueError(f"Unexpected token remaining after parsing: {self.current_token}")

        return result

    def parse_expression(self):
        left_node = self.parse_term()

        while self.current_token in [Op.ADD, Op.SUBTRACT]:
            op = self.current_token
            self.advance()
            right_node = self.parse_term()
            left_node = Operator(op, left_node, right_node)

        return left_node

    def parse_term(self):
        left_node = self.parse_unary()

        while self.current_token in [Op.MULTIPLY, Op.DIVIDE]:
            op = self.current_token
            self.advance()
            right_node = self.parse_unary()
            left_node = Operator(op, left_node, right_node)

        return left_node

    def parse_unary(self):
        if self.current_token in [Op.ADD, Op.SUBTRACT]:
            op = self.current_token
            self.advance()
            operand = self.parse_unary()
            return UnaryOp(op, operand)

        return self.parse_exponent()

    def parse_exponent(self):
        left_node = self.parse_factor()

        while self.current_token == Op.EXPONENT:
            op = self.current_token
            self.advance()
            right_node = self.parse_unary()
            left_node = Operator(op, left_node, right_node)

        return left_node

    def parse_factor(self):
        token = self.current_token

        if isinstance(token, Literal):
            self.advance()
            return token

        if isinstance(token, Variable):
            if token.name == 'diff':
                self.advance()

                if self.current_token != Op.LPAREN: raise ValueError("Expected '(' after diff")
                self.advance()

                expr = self.parse_expression()

                target_var = 'x'
                if self.current_token == Op.COMMA:
                    self.advance()

                    if isinstance(self.current_token, Variable):
                        target_var = self.current_token.name
                        self.advance()
                    else:
                        raise ValueError("Expected variable name after comma in diff")
                    
                if self.current_token != Op.RPAREN: raise ValueError("Missing ')' for diff")
                self.advance()

                return Diff(expr, target_var)

            self.advance()
            return token

        if self.current_token == Op.LPAREN:
            self.advance()
            result = self.parse_expression()

            if self.current_token == Op.RPAREN:
                self.advance()
                return result

            raise ValueError(f"Missing closing parenthesis")

        raise ValueError(f"Expected number, found {token}")
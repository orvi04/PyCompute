from ast_eval import Literal, Op, Operator


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
        return self.parse_expression()

    def parse_expression(self):
        left_node = self.parse_term()

        while self.current_token is not None and self.current_token in [Op.ADD, Op.SUBTRACT]:
            op = self.current_token
            self.advance()
            right_node = self.parse_term()
            left_node = Operator(op, left_node, right_node)

        return left_node

    def parse_term(self):
        left_node = self.parse_exponent()

        while self.current_token is not None and self.current_token in [Op.MULTIPLY, Op.DIVIDE]:
            op = self.current_token
            self.advance()
            right_node = self.parse_exponent()
            left_node = Operator(op, left_node, right_node)

        return left_node

    def parse_exponent(self):
        left_node = self.parse_factor()

        while self.current_token is not None and self.current_token == Op.EXPONENT:
            op = self.current_token
            self.advance()
            right_node = self.parse_factor()
            left_node = Operator(op, left_node, right_node)

        return left_node

    def parse_factor(self):
        token = self.current_token

        if isinstance(token, Literal):
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
from ast_eval import *

class Tokeniser:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[0] if text else None

    def advance(self):
        self.pos += 1
        if self.pos < len(self.text):
            self.current_char = self.text[self.pos]
        else:
            self.current_char = None

    def tokenise(self):
        tokens = []
        valid_ops = {member.value for member in Op}

        while self.current_char is not None:

            if self.current_char == " ":
                self.advance()
                continue

            if self.current_char in valid_ops:
                tokens.append(Op(self.current_char))
                self.advance()
                continue

            if self.current_char in "0123456789.":
                tokens.append(Literal(self.find_literal()))
                continue

            if self.current_char.isalpha():
                name = self.find_identifier()
                tokens.append(Variable(name))
                continue

            raise ValueError(f"Unknown character '{self.current_char}' at position {self.pos}")

        return tokens

    def find_literal(self):
        literal = []
        while self.current_char is not None and self.current_char in "0123456789.":
            literal.append(self.current_char)
            self.advance()
        return float("".join(literal))

    def find_identifier(self):
        chars = []
        while self.current_char is not None and self.current_char.isalnum():
            chars.append(self.current_char)
            self.advance()
        return "".join(chars)
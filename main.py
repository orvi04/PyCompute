from tokeniser import Tokeniser
from parser import Parser
from ast_eval import eval

def main():
    print("--- Python Calculator CLI ---")
    print("Type 'exit' or 'quit' to stop.")
    
    while True:
        try:
            # 1. Get Input
            text = input("calc> ")
            
            if text.lower() in ['exit', 'quit']:
                print("Goodbye!")
                break
            
            if not text.strip():
                continue

            # 2. Tokenise
            lexer = Tokeniser(text)
            tokens = lexer.tokenise()
            
            # 3. Parse
            parser = Parser(tokens)
            ast = parser.parse()
            
            # 4. Evaluate
            result = eval(ast)
            
            print(f"= {result}")

        except Exception as e:
            # Catch errors (Syntax, Math, etc.) and print them nicely
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
from tokeniser import Tokeniser
from parser import Parser
# Import evaluate and the custom exception
from ast_eval import eval, SymbolicResultError
# We still need simplify if we want to clean up the final symbolic output
from symbolic import simplify 

def main():
    print("--- Python CAS Calculator ---")
    print("Type 'exit' or 'quit' to stop.")
    
    while True:
        try:
            text = input("calc> ").strip()
            if text.lower() in ['exit', 'quit']: 
                print("Goodbye!")
                break
            if not text: continue

            lexer = Tokeniser(text)
            tokens = lexer.tokenise()
            
            parser = Parser(tokens)
            ast = parser.parse()
            
            # Attempt to evaluate everything
            result = eval(ast)
            
            # If successful (no exception raised), print the number
            print(f"= {result}")

        except SymbolicResultError as e:
            # If we catch the custom error, the result is the symbolic formula tree (e.node).
            
            # We simplify the result one last time before displaying
            final_formula = simplify(e.node) 
            
            print(f"= {final_formula}") 

        except Exception as e:
            # Catch all other unexpected/real errors
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
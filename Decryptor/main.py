from main_helpers import *
from settings import *

if __name__ == "__main__":

    loaded = None
    language_context = None
    saved_texts = dict()
    saved_texts_counter = 0
    help(["general_help"])
    command = prompt(loaded)

    while True:
        match command[0]:
            case "help":
                help(command[1:])
            
            case "encrypt":
                encrypted = encrypt(command[1:])

                if encrypted:
                    saved_texts[saved_texts_counter] = encrypted
                    print(f"\nResult saved at ({saved_texts_counter}):\n{encrypted}")
                    saved_texts_counter += 1    
            
            case "load":

                temp_loaded, temp_laco = load(command[1:])

                if temp_loaded:
                    loaded, language_context = temp_loaded, temp_laco

            case "solve":
                solve(command[1:], language_context, saved_texts)
                        
            case "exit":
                exit()
            
            case other:
                print_error(f"Unknown commnad '{other}'")
                print("* Type 'help' for more information")

        command = prompt(loaded)
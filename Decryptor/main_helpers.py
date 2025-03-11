from settings import *
from decryptor import *

help_texts = {
    "general_help":"""Decryptor 1.0
Usage: <command> [arguments]
commands:
\thelp <command|None>: shows info about command or general info
\tencrypt: Will show prompt for text and key
\tload <"czech"|"english"|file_name>: loads language context (dictionary)
\tsolve <saved_text|None>: will try to crack the text
\texit: exit""",

    "load": """Usage: 'load <"czech"|"english"|file_name>'
You can either use english or czech dictionaries that are saved already
or you can make your own .txt dictionary (you have to store it inside 'dictionaries' folder and then refer to it just by its name)
The dictionary should have all words on a new line.
Duplicates are allowed but can result in worse predictions.
Examples:
load czech
load english
load my_dict.txt""",

    "encrypt": """After typing encrypt you will be prompted for text and key
Your text will then be encrypted using vigenere cipher and provided key.
The result will be shown and also will be saved under some number 
so you don't have to copy it into your clipboard.
Beware! the key is not saved.
You can use this saved encrypted text when using 'solve' command like this:
'solve 1'
This will try to solve your encrypted text stored under number one.""",

    "exit": "Will exit the program",

    "solve": """Usage: 'solve <saved_text|None>'
This command will try to find the vigenere key through the provided text.
After some results are found they will be shown.""",
    "help": "I have no idea what could 'help' mean. Sorry",

    "timeSpent":
    """To much to count"""
}


def help(command):
    if len(command) == 0:
        print(help_texts["general_help"])
        return
    
    if len(command) >= 2:
        print_error("More than one commands given")
    
    if command[0] in help_texts:
        print(help_texts[command[0]])
    else:
        print_error(f"Command '{command[0]}' not found")

def prompt(loaded):
    command = input(f"\n╔═══(loaded: {loaded})\n╚═Decrypted> ")
    print()
    if not command:
        return [""]
    return command.split()

def print_error(error):
    print('\033[91m' + error + '\033[0m')

def get_text():
    print("Enter Text: (supports all characters including new line, empty line to finish)")
    result = [input("│ ").strip()]
    while result[-1] != "":
        result.append(input("│ ").strip())
    print("└──")
    del result[-1]

    return " \n".join(result)

def load(data):
    if len(data) == 0:
        print_error("Language context not given")
        print("* Usage: 'load <czech|english|relative_path>'")
        print("* For example 'load czech'")
        return (None, None)
    
    if len(data) > 1:
        print_error("Multiple contexts given")
        print("* Usage: 'load <czech|english|relative_path>'")
        print("* For example 'load czech'")
        return (None, None)
    
    if data[0] in SAVED_DICTIONARIES:
        loaded = data[0]
        print("\rLoading language context ...", end="")
        language_context = LanguageContext(SAVED_DICTIONARIES[loaded])
        print("\033[92mDone\033[0m")
        return (loaded, language_context)
    
    if data[0][-4:] != ".txt":
        data[0] += ".txt"

    try:
        with open("./dictionaries/" + data[0], "r") as file:
            pass
    except:
        print_error("Couldn't locate/open the file")
        return (None, None)
        
    print("\rLoading language context...", end="")
    language_context = LanguageContext("./dictionaries/" + data[0])
    print("\033[92mDone\033[0m")
    loaded = data[0]
    return (loaded, language_context)

def encrypt(data):
    if data:
        print_error("Please provide the text after typing encrypt")
        return
    
    text = get_text()
    
    if not text:
        print_error("No text given")
        return
    
    key = input("key (including spaces): ").strip()

    if not key:
        print_error("No key given")
        return

    return vigenere_encrypt(text, key)
    

def solve(data, language_context, saved_texts):
    if not language_context:
        print_error("No language context specified")
        return
    
    if len(data) == 0:
        text = get_text()
        if not text:
            print_error("No text given")
            return
        solver = CipherSolver(text, language_context)

    elif len(data) == 1 and data[0].isdigit():
        if int(data[0]) in saved_texts:
            solver = CipherSolver(saved_texts[int(data[0])], language_context)
        else:
            print_error(f"{data[0]} not found in saved")
            return         
    else:
        print_error(f"Not valid number for saved_text given: {''.join(data)}")
        return
    

    

    
    #if len(data) == 1 and data[0].isdigit():
    #    if int(data[0]) in saved_texts:
    #        solver = CipherSolver(saved_texts[int(data[0])], language_context)
#
    #    else:
    #        print_error(f"{data[0]} not found in saved")
    #        return
    #    
    #else:
    #    
    #    solver = CipherSolver(" ".join(data), language_context)
    #
    print("\rSolving...", end="")
    solver.solve()
    print("\033[92mDone\033[0m\n")

    print(solver.get_result(solver.result_heap.pop()))

    another = solver.result_heap.pop()
    if another:
        decision = input("Show all results? (y/n) ").strip().lower()
        if decision == "y":
            while another:
                print(another)
                another = solver.get_result(solver.result_heap.pop())
    return

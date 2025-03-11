"""
tento soubor obsahuje všechny konfigurace a nastavení
"""
from string import ascii_lowercase as all_characters

# NEMĚNIT
ALL_CHARACTERS = all_characters # abeceda seřazená abecedně
ALPHABET_LENGTH = 26

MAX_WORDTREE_DISTANCE = 3 # maximální počet modifikací při hledání správného slova
MAX_VIGENERE_KEY_LENGTH = 8 # maximální hledaná délka klíče
APPLY_POST = True # použít nebo nepoužít post vigenere

# nastavení pro vypisování výsledků
TEXT_PRINT_SIZE = 200 # délka vypsání výsledků
CHANCE_ROUND = 3 # zaokrouhlení šance výsledku

SAVED_DICTIONARIES = {
    "czech": "./dictionaries/czech.txt",
    "english": "./dictionaries/english.txt"
}

CZECH_DICT_RELATIVE_PATH = "./dictionaries/czech.txt"
ENGLISH_DICT_RELATIVE_PATH = "./dictionaries/english.txt"
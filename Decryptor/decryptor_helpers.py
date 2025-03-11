from string import ascii_lowercase as all_characters
from settings import *
import heapq

class WordNode:
    
    def __init__(self, character, is_word):
        self.character = character
        self.is_word = is_word
        self.next_characters = dict()

class WordTree:
    def __init__(self):
        self.start = WordNode("", False)

    def add_word(self, word):
        """
        in - word (string)
        out - None

        postupně projde na pozici svého slova a následně označí místo jako slovo
        """
        node = self.start

        for character in word:
            if character not in node.next_characters:
                node.next_characters[character] = WordNode(character, False)
            
            node = node.next_characters[character]
        
        node.is_word = True


    def is_word(self, word):
        """
        in - word (string)
        out - je/není slovo (boolean)

        Budeme procházet stejně jako při přidávání.
        Pokud se budeme chtít dostat někde, kde není cesta
        víme, že slovo neexistuje
        """
        node = self.start

        for character in word:
            if character not in node.next_characters:
                return False

            node = node.next_characters[character]
        
        return node.is_word
    
    def nearest_words(self, word, first_k, max_distance=MAX_WORDTREE_DISTANCE):
        """
        in  - word (string)         hledáme nejbižší slova tomuto
            - first_k (int)         hledáme k nejbližších
            - max_distance (int)    maximální počet modifikací

        out - list s prvky (word, distance)

        !! nepodporuje mazání a přidávání písmen, pouze modifikace !!
        """
        
        nearest_words = set()

        def recur(node, distance, word_now, max_distance):
            if distance > max_distance:
                return
            
            if len(nearest_words) >= first_k:
                return
            
            if len(word_now) == len(word):
                if node.is_word:
                    nearest_words.add((word_now, distance))
                return
            
            for next_char in ALL_CHARACTERS:
                if next_char in node.next_characters:
                    if next_char == word[len(word_now)]:
                        recur(node.next_characters[next_char],
                              distance,
                                word_now+ next_char,
                                max_distance
                                )
                    else:
                        recur(node.next_characters[next_char],
                              distance+1,
                                word_now+ next_char,
                                max_distance
                                )

        for up_to_distance in range(0, max_distance):
            recur(self.start, 0, "", up_to_distance)

        if len(nearest_words) == 0:# pokud nenajdeme žádné blízké slovo
        
            return [(word, len(word))]
        
        return sorted(nearest_words, key=lambda a: a[1])[:first_k]




    

class Result:
    """
    slouží především pro přehlednější ukládání výsledků a manipulaci s nimi
    """
    def __init__(self):
        self.chance = None
        self.text = None
        self.key = None
        self.inverse_key = None
        self.method = None

    def __lt__(self, other): # mělo by být __gt__ ale heapq dělá min haldu a nechce se mi už hledat jak to měnit
        if self.chance == other.chance:
            return len(self.key) < len(other.key)
        return self.chance > other.chance


    def __repr__(self):

        return f"method:\t {self.method}\nchance:\t {int(self.chance*100)}%\nencryption key:\t {self.key}\ndecryption key:\t {self.inverse_key}\ntext:\n{self.text[:TEXT_PRINT_SIZE]}\n"

class ResultHeap:
    def __init__(self):
        self.heap = []
        self.best_chance = 0
    
    def insert(self, result):
        if result.chance > self.best_chance:
            self.best_chance = result.chance
        heapq.heappush(self.heap, result)

    def pop(self):
        if len(self.heap) == 0:
            return None
        return heapq.heappop(self.heap)
    
    def clear(self):
        self.heap.clear()

    

class LanguageContext:
    """
    - Třída LanguageContext obsahuje informace o jazyce nezašifrovaného textu
    - Třída je navrhnutá tak, aby po dodání slovníku byla schopna pomoct rozšifrovat
      jakýkoliv jazyk (i vymyšlený (pokud se dá zapsat v ascii))
    """
    def __init__(self, dictionary_path):

        self.word_tree = WordTree()

        with open(dictionary_path, "r") as file:
            for word in [line.rstrip() for line in file]:
                self.word_tree.add_word(word)

        with open(dictionary_path, "r") as file:
            self.char_distribution = text_char_distribution(file.read())
           






def char_to_num(char):
    # změní znak na pozici v abecedě (s indexem 0)
    return ord(char) - ord("a")

def num_to_char(num):
    # změní číslo na znak
    return chr(ord("a") + num)

def shift_char(char, shift):
    # posune charakter (string) o shift znaků doprava
    # při přetečení skočí na začátek abecedy (jako zbytková třída)
    return num_to_char((char_to_num(char) + shift)%ALPHABET_LENGTH)

def inverse_key(key):
    """
    pro daný klíč vygeneruje inverzní klíč
    při aplikování klíče a potom aplikaci jeho inverzního klíče dostaneme původní text
    """

    if len(key) == 1:
        return num_to_char((-char_to_num(key))%ALPHABET_LENGTH)

    else:
        return "".join(inverse_key(char) for char in key)


def caesar_encrypt(text, shift):
    """
    in  - text (string) který chceme zašifrovat
        - shift (string) o kolik chceme každý znak posunout doprava (a -> b)

    out - zašifrovaný text
    """
    text = text.lower().strip()
    res = ""

    for char in text:
        if not char.isalpha():
            res += char
        else:
            res += shift_char(char, shift)

    return res

def vigenere_encrypt(text, key):
    """
    in  - text (string) který chceme zašifrovat
        - key (string) klíč kterým zašifrujeme (vysvětlení v dokumentaci)
    
    out - zašifrovaný text
    """
    text = text.lower().strip()
    key = key.lower().strip()

    key_index = 0
    res = ""

    for char in text:
        if not char.isalpha():
            res += char
        else:
            res += shift_char(char, char_to_num(key[key_index]))

            key_index = (key_index+1)%len(key)

    return res


def text_char_distribution(text):
    """
    vrátí slovník {znak: procento výskytu}
    procento výskytu je hodnota 0 až 1
    """
    distribution = dict()
    text_length = 0 # nemůžeme počítat přes len() protože by se započítaly mezery

    for character in ALL_CHARACTERS:
        distribution[character] = 0 

    if len(text) == 0: 
        return distribution

    for character in text:

        if character.isalpha():
            text_length += 1
            distribution[character] += 1


    for character in ALL_CHARACTERS:
        distribution[character] /= text_length

    return distribution

def root_of_key(key):
    """
    vrátí opakující se sekvenci klíče
    pro "asdasdasdasd" vrátí "asd"
    """
    temp = (key + key).find(key, 1, -1)
    if temp != -1: 
        return key[:temp]
    return key

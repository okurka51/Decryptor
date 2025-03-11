from decryptor_helpers import *
from settings import *

class CipherSolver:
    """
    Hlavní třída pro dešifrování

    """

    def __init__(self, encrypted_text, language_context, applyPost=APPLY_POST):

        # uložení a odstranění nonAlpha znaků (kromě mezer)
        self.non_alpha = []
        correct_text = ""
        for char_index in range(len(encrypted_text)):
            if (not encrypted_text[char_index].isalpha()) and encrypted_text[char_index] != " ":
                self.non_alpha.append((char_index, encrypted_text[char_index]))
            else:
                correct_text += encrypted_text[char_index]

        self.encrypted_text = correct_text
        self.language_context = language_context
        self.result_heap = ResultHeap()
        self.applyPost = applyPost


    def best_caesar_shift(self, text):
        """
        Pro daný text najde nejlepší caesarový posun tak,
        aby se co jak nejméně lišil od jazyka v language_context
        Vrací int
        """

        best_shift = 0
        smallest_difference = float("inf")
        char_distribution_of_text = text_char_distribution(text)

        for shift in range(ALPHABET_LENGTH): # zkoušíme každý posun
            difference = 0

            for character in ALL_CHARACTERS: # suma rozdílů všech písmen
                difference += abs(
                    char_distribution_of_text[shift_char(character, -shift)]
                    - self.language_context.char_distribution[character]
                )

            if smallest_difference > difference:
                smallest_difference = difference
                best_shift = shift
            
        return best_shift


    def vigenere_decrypt(self, text):
        """
        Vygeneruje takové klíče, aby po jejich aplikaci výsledný text co jak nejvíce 
        korespondoval s distribucí jazyka v language_context
        funguje na základě funkce best_caesar_shift
        Zkoušíme všechny možné (povolené) délky klíče
        """
        shift_list = []
        non_alpha = []
        correct_text = ""


        # odstranění mezer znaků
        for char_index in range(len(text)):
            if not text[char_index].isalpha():
                non_alpha.append((char_index, text[char_index]))
            else:
                correct_text += text[char_index]
        text = correct_text



        for possible_key_length in range(1, MAX_VIGENERE_KEY_LENGTH): # všechny povolené délky klíče
            good_shift = []

            for kth_characters in range(possible_key_length):
                # každý znak klíče se při šifrování aplikuje na znaky textu, 
                # které jsou od sebe daleko o velikost klíče 
                best_shift = self.best_caesar_shift(text[kth_characters::possible_key_length])
           
                good_shift.append(best_shift)

     
            
            shift_list.append(good_shift)

        # vrácení mezer znaků
        for index, character in non_alpha:
            text = text[:index] + character + text[index:]

        
        for shift in shift_list: # ukládání každého výsledku
            res = Result()

            res.inverse_key = root_of_key("".join(num_to_char(char) for char in shift))            
            res.key = inverse_key(res.inverse_key)
            res.text = vigenere_encrypt(text, res.inverse_key)
            res.chance = self.text_score(res.text, False)
            res.method = "vigenere"

            self.result_heap.insert(res)

            # pokud jsme povolili post_vigenere zavoláme jej na každý z výsledků
            if self.applyPost:
                self.result_heap.insert(self.post_vigenere(res))


    def post_vigenere(self, raw_result):
        """
        post_vigenere vezme výsledek z vigenere_decrypt, který často není dokonalý,
        protože správná distribuce znaků skoro nikdy nezaručí správný výsledek.
        Post_vigenere proto vezme nedokonalý výsledek a zkusí zvlášť každý znak klíče
        posunout tak, abychom změnili nedokonalé slovo textu na jemu nejbližší slovo.  
        """

        best_chance = raw_result.chance
        best_text = raw_result.text
        best_shift = ["a" for _ in raw_result.key] # klíč, který nic nezmění
        
        for shift_index in range(len(raw_result.key)): # kterou část klíče chceme modifikovat
            new_shift = best_shift.copy()

            for shift in ALL_CHARACTERS: # pro každou pozici zkusíme každé posunutí
                new_shift[shift_index] = shift
                new_text = vigenere_encrypt(raw_result.text, "".join(new_shift))
                
                new_chance = self.text_score(new_text, True)
                
                # pokud ohodnocení nového textu je lepší než dosavadní, nový posun brát jako správný
                if new_chance > best_chance:
                    best_chance = new_chance
                    best_text = new_text
                    best_shift[shift_index] = shift

        # ukládání výsledku
        res = Result()
        # nový klíč je jenom modifikace toho starého
        # proto můžeme na ten starý použít vigenere_encrypt pro posun
        res.inverse_key = root_of_key(vigenere_encrypt(raw_result.inverse_key, "".join(best_shift)))
        res.key = inverse_key(res.inverse_key)
        res.text = best_text
        res.chance = self.text_score(res.text, False)
        res.method = "post_vigenere"

        return res

    def word_score(self, word, internal):
        """
        Ohodnocovací funkce slov, která má dva "módy"
        Obecně word_score říká jestli nebo jak moc je nějaké slovo správné

        internal == True:
            - ohodnotí každé slovo podle toho, jak moc je blízko správnému slovu
            - např. pro "mazlo" (maslo) vrátí 0.8 -> musíme podifikovat jedno písmeno
            - vhodný spíše pro post_vigenere, kde postupná modifikace ze začátku vetšinou
              nevytvoří správná slova
            - nehodí se pro ohodnocování celých textů (např. ve výsledku) protože pro texty
              kde není žádné slovo správné, ale každé je blízko nějakému správnému vrací vysoké hodnoty
            - pomalejší

        internal == False:
            - ohodnotí každé slovo jako 0/1 podle toho jestli je slovem nebo ne
            - hodí se při počítání šance výsledku
            - rychlejší
        """
        if len(word) == 0:
            return 0

        if internal:
            correct_word, distance = self.language_context.word_tree.nearest_words(word, 1)[0]
            return (len(word)-distance)/len(word)
        
        return 1 * self.language_context.word_tree.is_word(word)
    
    def text_score(self, text, internal):
        """
        Ohodnocující funkce na základě word_score
        """
        score = 0

        if len(text) == 0:
            return 0

        text = text.split()
        for word in text:
            score += self.word_score(word, internal)
        
        return (score/len(text))
    
    def solve(self):
        self.vigenere_decrypt(self.encrypted_text)

    def get_result(self,result):
        if not result:
            return None
        
        # vrácení mezer
        text = result.text
        for index, character in self.non_alpha:
            text = text[:index] + character + text[index:]

        return f"method:\t {result.method}\nchance:\t {int(result.chance*100)}%\nencryption key:\t {result.key}\ndecryption key:\t {result.inverse_key}\ntext:\n{text[:TEXT_PRINT_SIZE]}\n"

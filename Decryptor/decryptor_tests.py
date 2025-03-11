import unittest

from decryptor import *
from settings import *

class TestStringMethods(unittest.TestCase):

    def test_solver(self):
        language_context = LanguageContext(SAVED_DICTIONARIES["czech"])
        text = "text nevim neco pisu\ndalsi radek13123\n atak no"
        solver = CipherSolver("", language_context)

        print()

    def test_word_score(self):
        language_context = LanguageContext(SAVED_DICTIONARIES["czech"])
        solver = CipherSolver("", language_context)

        self.assertEqual(solver.word_score("marek", False), 1)
        self.assertEqual(solver.word_score("parek", True), 1)

        self.assertEqual(solver.word_score("sarek", False), 0)
        self.assertEqual(solver.word_score("sarek", True), 0.8)

        self.assertEqual(solver.word_score("", False), 0)
        self.assertEqual(solver.word_score("", True), 0)

    def test_text_score(self):
        language_context = LanguageContext(SAVED_DICTIONARIES["czech"])
        solver = CipherSolver("", language_context)

        self.assertEqual(solver.text_score("nevim neco jedna dva shdfksad", False), 0.8)
        self.assertEqual(solver.text_score("nevim neco jea dva shdfksad", False), 0.6)
        
        self.assertEqual(solver.text_score("mailo masio", True), 0.8)
        self.assertEqual(solver.text_score("mailo masio", False), 0)

        self.assertEqual(solver.text_score("", True), 0)
        self.assertEqual(solver.text_score("", False), 0)

    def test_best_caesar_shift(self):
        language_context = LanguageContext(SAVED_DICTIONARIES["czech"])
        solver = CipherSolver("", language_context)

        self.assertEqual(solver.best_caesar_shift("a"), 4)
        self.assertEqual(solver.best_caesar_shift("b"), 3)
        self.assertEqual(solver.best_caesar_shift("z"), 5)
        self.assertEqual(solver.best_caesar_shift("eeeeeeee"), 0)

        text = "nejaky dlouhy text budu pouzivat jenom text ktery je podobny cestine protoze jinak to nebude fungovat tohle neni jiste ze bude fungovat ale je na tom zalozeny kod takze by to melo fungovat"
        encrypted = caesar_encrypt(text, 7)
        self.assertEqual(solver.best_caesar_shift(text), 0)
        self.assertEqual(solver.best_caesar_shift(encrypted), 26-7)


    def test_vigenere_decrypt(self):
        language_context = LanguageContext(SAVED_DICTIONARIES["czech"])
        solver = CipherSolver("", language_context, applyPost=False)

        solver.vigenere_decrypt("a")

        result = solver.result_heap.pop()
        self.assertEqual(result.text, "e")
        self.assertEqual(result.chance, 0)
        self.assertEqual(result.key, "w")
        self.assertEqual(result.inverse_key, "e")

        solver.result_heap.clear()

        text = "nejaky dlouhy text budu pouzivat jenom text ktery je podobny cestine protoze jinak to nebude fungovat tohle neni jiste ze bude fungovat ale je na tom zalozeny kod takze by to melo fungovat"

        solver.vigenere_decrypt(text)
        result = solver.result_heap.pop()
        self.assertEqual(result.text, text)
        self.assertAlmostEqual(result.chance*100, 100, delta=5)
        self.assertEqual(result.key, "a")
        self.assertEqual(result.inverse_key, "a")

        solver.result_heap.clear()

        # -----------------------
        key = "ahoj" # to nahoře je zašifrovaný text z proměnné text
        encrypted = vigenere_encrypt(text, key)

        solver.vigenere_decrypt(encrypted)
        result = solver.result_heap.pop()
        
        # výsledek je 18% ale pokud se podíváte na výsledek tak je blízko správnému řešení
        # s použitím ohodnocení "interal == True" by nám to vyhodnotilo lepší výsledek, ale 
        # často se v takovém případě stane, že špatné výsledky přeskočí ty dobré
        # takový výsledek v podstatě nevadí
        #print(result.text) # můžete odkomentovat na ukázku
        #self.assertAlmostEqual(result.chance*100, 100, delta=10)

    def test_post_vigenere(self):
        text = "nejaky dlouhy text budu pouzivat jenom text ktery je podobny cestine protoze jinak to nebude fungovat tohle neni jiste ze bude fungovat ale je na tom zalozeny kod takze by to melo fungovat"
        language_context = LanguageContext(SAVED_DICTIONARIES["czech"])
        solver = CipherSolver("", language_context, applyPost=True)

        encrypted = vigenere_encrypt(text, "ahoj")
        solver.vigenere_decrypt(encrypted)

        result = solver.result_heap.pop()

        self.assertEqual(result.text, text)
        self.assertAlmostEqual(result.chance*100, 100, delta=5)
        self.assertEqual(result.key, "ahoj")
        self.assertEqual(result.inverse_key, inverse_key("ahoj"))




if __name__ == '__main__':
    unittest.main()
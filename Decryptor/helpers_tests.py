import unittest
from decryptor_helpers import *
from settings import *

class TestStringMethods(unittest.TestCase):

    def test_char_to_num(self):
        self.assertEqual(char_to_num("a"), 0)
        self.assertEqual(char_to_num("c"), 2)
        self.assertEqual(char_to_num("z"), 25)

    def test_num_to_char(self):
        self.assertEqual(num_to_char(0), "a")
        self.assertEqual(num_to_char(2), "c")
        self.assertEqual(num_to_char(25), "z")

    def test_shift_char(self):
        self.assertEqual(shift_char("a", 0), "a")
        self.assertEqual(shift_char("b", 1), "c")
        self.assertEqual(shift_char("z", 1), "a")
        self.assertEqual(shift_char("y", 3), "b")
        self.assertEqual(shift_char("b", -2), "z")

    def test_inverse_key(self):
        self.assertEqual(inverse_key("a"), "a")
        self.assertEqual(inverse_key("b"), "z")
        self.assertEqual(inverse_key("c"), "y")
        self.assertEqual(inverse_key("aaa"), "aaa")
        self.assertEqual(inverse_key("abc"), "azy")

    def test_caesar_encrypt(self):
        self.assertEqual(caesar_encrypt("a", 1), "b")
        self.assertEqual(caesar_encrypt("b", -1), "a")
        self.assertEqual(caesar_encrypt("bcd", 1), "cde")
        self.assertEqual(caesar_encrypt("bcd", 3), "efg")

    def test_vigenere_encrypt(self):
        self.assertEqual(vigenere_encrypt("a", "a"), "a")
        self.assertEqual(vigenere_encrypt("marek", "a"), "marek")
        self.assertEqual(vigenere_encrypt("marek", "b"), "nbsfl")
        self.assertEqual(vigenere_encrypt("aaaaa", "marek"), "marek")
        self.assertEqual(vigenere_encrypt("abcd", "bbbbbbbbbbbb"), "bcde")

    def test_text_char_distribution(self):
        base_dictionary = dict()
        for character in ALL_CHARACTERS:
            base_dictionary[character] = 0

        temp_dictionary = base_dictionary.copy()
        temp_dictionary["a"] = 1
        self.assertEqual(text_char_distribution("a"), temp_dictionary)

        temp_dictionary = base_dictionary.copy()
        temp_dictionary["a"] = 1/4
        temp_dictionary["b"] = 1/4
        temp_dictionary["c"] = 1/4
        temp_dictionary["d"] = 1/4
        self.assertEqual(text_char_distribution("a  b c  \n /d }[@}]"), temp_dictionary)

        temp_dictionary = base_dictionary.copy()
        temp_dictionary["a"] = 1
        self.assertEqual(text_char_distribution("aa aaaaaaaaa   "), temp_dictionary)
        
    def test_root_of_key(self):
        self.assertEqual(root_of_key("nevim"), "nevim")
        self.assertEqual(root_of_key("nevimnevim"), "nevim")
        self.assertEqual(root_of_key("nevimneim"), "nevimneim")
        self.assertEqual(root_of_key("h"), "h")
        self.assertEqual(root_of_key(""), "")
        self.assertEqual(root_of_key("aaaaaaaaaaa"), "a")

    def test_word_tree(self):
        word_tree = WordTree()
        all_words = []
        with open("./dictionaries/czech.txt", "r") as file:
            for word in [line.rstrip() for line in file]:
                word_tree.add_word(word)
                all_words.append(word)
            
        for word in all_words:
            self.assertEqual(word_tree.is_word(word), True)

        self.assertEqual(word_tree.nearest_words("mailo", 1), [("maslo", 1)])
        self.assertEqual(word_tree.nearest_words("spravne", 1), [("spravne", 0)])

        one_letter_words = set((("a",1),("i",1),("o",1),("u",1),("s",1),("v",1),("k",1),("z",1)))
        self.assertEqual(set(word_tree.nearest_words("x", 20)), one_letter_words) # set protože nevím pořadí

        # změnil jsem dva písmena toho slova
        # u menších slov se může najít shoda s jinými slovy (což není chyba ale špatně se to testuje)
        #                                                             ↓     ↓
        #                                         nejnezdevetadevadesateroroznasobovavatelnejsi
        self.assertEqual(word_tree.nearest_words("nejnezdevetadevadesarerorosnasobovavatelnejsi", 1), [("nejnezdevetadevadesateroroznasobovavatelnejsi", 2)])

    def test_heap(self):
        res1 = Result()
        res1.chance = 1
        res1.key = "jedna"

        res2 = Result()
        res2.chance = 2
        res2.key = "asdasdasdasdasdasdasdasdasdasd"

        res3 = Result()
        res3.chance = 2
        res3.key = "asd"

        res4 = Result()
        res4.chance = 4
        res4.key = "jedna"

        heap = ResultHeap()

        heap.insert(res1)
        heap.insert(res4)
        heap.insert(res2)
        heap.insert(res3)


        self.assertEqual(heap.pop().chance, 4)
        self.assertEqual(heap.pop().key, "asd")
        self.assertEqual(heap.pop().key, "asdasdasdasdasdasdasdasdasdasd")
        self.assertEqual(heap.pop().chance, 1)


if __name__ == '__main__':
    unittest.main()
import os
import sys
import unittest
from pprint import pprint


sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from ukrainian_accentor_transformer import Accentor


class TestAccentor(unittest.TestCase):

    @classmethod
    def setUpClass(TestAccentor):
        TestAccentor.accentor = Accentor()

    def test_simple_accent(self):
        text = "Привіт хлопче, як справи."
        accented = self.accentor(text)
        self.assertEqual(text, accented.replace("\u0301",""))

    def test_batch_accent(self):
        text1 = "Привіт хлопче, як справи."
        text2 = "в мене все добре, дякую."
        accented1, accented2 = self.accentor([text1, text2])
        self.assertEqual(text1, accented1.replace("\u0301",""))
        self.assertEqual(text2, accented2.replace("\u0301",""))


if __name__ == '__main__':
    unittest.main()
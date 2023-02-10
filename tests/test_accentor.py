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

    def test_long_sentence(self):
        text = "Адже як би не оцінював галичан один страшно інтелігентний виходець з радянсько єврейських середовищ київського Подолу самі галичани вважають свою культуру і традицію політичну і релігійну побутову й господарську на голову вищою від усього що за Збручем"
        accented = self.accentor(text)
        self.assertEqual(text, accented.replace("\u0301",""))

    def test_long_sentence(self):
        text = "Веселка також райдуга атмосферне оптичне явище що являє собою одну дві чи декілька спектральних дуг або кіл якщо дивитися з повітря що спостерігаються на тлі хмари якщо вона розташована проти Сонця Червоний колір спектру ми бачимо з зовнішнього боку первинної веселки а фіолетовий із внутрішнього"
        accented = self.accentor(text)
        self.assertEqual(text, accented.replace("\u0301",""))

if __name__ == '__main__':
    unittest.main()

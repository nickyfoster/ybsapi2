import unittest


class TestFisrt(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.a = 5
        cls.b = 4

    def test_tfidf_kwe(self):
        res = self.a + self.b
        self.assertEqual(res, 9)

import unittest


class TestPython(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.a = 5
        cls.b = 4

    def test_python(self):
        res = self.a + self.b
        self.assertEqual(res, 9)

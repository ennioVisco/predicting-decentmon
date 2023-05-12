import unittest

from decmon.normalizer import normalize


class TestNormalizer(unittest.TestCase):
    # Formulas
    f1 = "Or (a, b)"
    f2 = "Or (Or (a, c), b)"
    f3 = "And (a, b)"
    f4 = "Imp (a, b)"
    f5 = "Iff (a, b)"
    f6 = "And (Or (a, b), c)"
    f7 = "Glob (a)"
    f8 = "Xor (a, b)"
    f9 = "Ev (a)"
    # Normalized formulas
    f1n = "Neg (And (Neg (a), Neg (b)))"
    f2n = "Neg (And (Neg (Neg (And (Neg (a), Neg (c)))), Neg (b)))"
    f3n = "And (a, b)"
    f4n = "Neg (And (Neg (Neg (a)), Neg (b)))"
    f5n = "And (Neg (And (Neg (Neg (a)), Neg (b))), Neg (And (Neg (Neg (b)), Neg (a))))"
    f6n = "And (Neg (And (Neg (a), Neg (b))), c)"
    f7n = "Neg (Until (True, Neg (a)))"
    f8n = "Neg (And (Neg (And (a, Neg (b))), Neg (And (b, Neg (a)))))"
    f9n = "Until (True, a)"

    def test_normalize_f1(self):
        self.assertEqual(self.f1n, normalize(self.f1))

    def test_normalize_f2(self):
        self.assertEqual(self.f2n, normalize(self.f2))

    def test_normalize_f3(self):
        self.assertEqual(self.f3n, normalize(self.f3))

    def test_normalize_f4(self):
        self.assertEqual(self.f4n, normalize(self.f4))

    def test_normalize_f5(self):
        self.assertEqual(self.f5n, normalize(self.f5))

    def test_normalize_f6(self):
        self.assertEqual(self.f6n, normalize(self.f6))

    def test_normalize_f7(self):
        self.assertEqual(self.f7n, normalize(self.f7))

    def test_normalize_f8(self):
        self.assertEqual(self.f8n, normalize(self.f8))

    def test_normalize_f9(self):
        self.assertEqual(self.f9n, normalize(self.f9))

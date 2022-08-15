import unittest

from decmon.extractor import *


class TestExtractor(unittest.TestCase):
    test_string = 'Until (Ev (Var "b"), And (Var "c", Var "a"))'

    def tests_it_works(self):
        self.assertEqual(True, True)

    def tests_finds_single_op(self):
        self.assertEqual(1, count_op("Until", self.test_string))

    def tests_finds_multiple_ops(self):
        self.assertEqual(3, count_op("Var", self.test_string))

    def tests_finds_temporal_ops(self):
        actual_sum = sum(count_set_ops(temporal_operators, self.test_string))
        self.assertEqual(2, actual_sum)

    def tests_finds_classic_ops(self):
        actual_sum = sum(count_set_ops(classic_operators, self.test_string))
        self.assertEqual(1, actual_sum)

    def tests_finds_all_ops(self):
        ops_counts = count_all_ops(self.test_string)
        clustered_ops_counts = list(map(sum, ops_counts))
        self.assertEqual(6, sum(clustered_ops_counts))

    def tests_finds_all_the_right_ops(self):
        ops_counts = count_all_ops(self.test_string)
        self.assertEqual([0, 0], ops_counts[0])
        self.assertEqual([3], ops_counts[1])
        self.assertEqual([1, 0, 0, 0, 0, 0], ops_counts[2])
        self.assertEqual([1, 0, 1, 0, 0, 0], ops_counts[3])

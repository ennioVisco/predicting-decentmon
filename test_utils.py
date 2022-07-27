import unittest

from utils import count_op, count_set_ops, count_all_ops, temporal_operators, classic_operators


class MyTestCase(unittest.TestCase):
    test_string = 'Until (Ev (Var "b"), And (Var "c", Var "a"))'

    def tests_work(self):
        self.assertEqual(True, True)  # add assertion here

    def tests_finds_single_op(self):
        self.assertEqual(1, count_op("Until", self.test_string))

    def tests_finds_multiple_ops(self):
        self.assertEqual(3, count_op("Var", self.test_string))

    def tests_finds_temporal_ops(self):
        self.assertEqual(2, sum(count_set_ops(temporal_operators, self.test_string)))

    def tests_finds_classic_ops(self):
        self.assertEqual(1, sum(count_set_ops(classic_operators, self.test_string)))

    def tests_finds_all_ops(self):
        ops_counts = count_all_ops(self.test_string)
        clustered_ops_counts = list(map(sum, ops_counts))
        self.assertEqual(6, sum(clustered_ops_counts))


if __name__ == '__main__':
    unittest.main()

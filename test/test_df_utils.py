import unittest

import pandas as pd
import os

from decmon.constants import INPUT_DIR
from decmon.df_utils import extract_ops, load_simulation_data, extract_metrics


class TestDfUtils(unittest.TestCase):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    df = pd.DataFrame(
        {'formula': ['Var "a"', 'Var "b"'],
         'id': ['a', 'b'],
         })
    values = [1, 2, 3]
    df2 = pd.DataFrame(
        {
            'trace_len': values,
            'num_mess': values,
            'size_mess': values,
            'nb_progressions': values,
            'formula_id': [1, 2, 3],
            'strategy': ['a', 'b', 'c'],
         })

    def test_extract_ops_from_simple_formula(self):
        ops = extract_ops(self.df)
        self.assertEqual(2, len(ops))

    def test_load_simulation_data(self):
        df = load_simulation_data(f'{self.dir_path}/../{INPUT_DIR}/sample_log.txt')
        self.assertEqual(27, len(df))

    def test_extract_metrics_correctly(self):
        extracted = extract_metrics(self.df2)

        self.assertEqual(4 * len(self.values), len(extracted['value']))
        self.assertEqual(self.values, extracted['value'].unique().tolist())
        self.assertEqual(4, len(extracted['metric'].unique()))

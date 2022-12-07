import unittest

import pandas as pd

from decmon.constants import INPUT_DIR, STRATEGIES
from decmon.df_utils import extract_ops, load_simulation_data


class TestDfUtils(unittest.TestCase):
    df = pd.DataFrame(
        {'formula': ['Var "a"', 'Var "b"'],
         'id': ['a', 'b'],
         })

    def test_extract_ops_from_simple_formula(self):
        ops = extract_ops(self.df)
        self.assertEqual(2, len(ops))

    def test_load_simulation_data(self):
        df = load_simulation_data(f'../{INPUT_DIR}/sample_log.txt')
        self.assertEqual(27, len(df))

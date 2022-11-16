import unittest

import pandas as pd

from decmon.df_utils import extract_ops


class TestDfUtils(unittest.TestCase):
    df = pd.DataFrame(
        {'formula': ['Var a', 'Var b'],
         })

    # def test_extract_ops_from_simple_formula(self):
    #     ops = extract_ops(self.df)
    #     self.assertEqual(2, len(ops))
    #     self.assertEqual(51, len(ops.columns))
    #
    #     self.assertEqual("Next", ops[0])

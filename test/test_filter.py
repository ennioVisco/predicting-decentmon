import unittest

import pandas as pd

from decmon.filter import exclude_annotate


class TestCleaner(unittest.TestCase):
    df = pd.DataFrame(
        {'numbers': [1, 2, 3],
         'colors': ['c_red', 'c_white', 'c_blue'],
         'numbers2': [1, 2, 3]
         })

    def test_filter_numbers_as_strategy(self):
        match = "numbers"
        filtered = exclude_annotate(self.df, match, match)
        self.assertEqual(2, len(filtered.columns))
        self.assertEqual("strategy", filtered.columns[-1])
        self.assertNotIn("numbers", filtered.columns[0])

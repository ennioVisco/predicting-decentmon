import unittest

import pandas as pd

from decmon.filter import exclude_annotate, select_metric, split_by_dictionary


class TestCleaner(unittest.TestCase):
    df = pd.DataFrame(
        {'numbers': [1, 2, 3],
         'colors': ['c_red', 'c_white', 'c_blue'],
         'numbers_2': [1, 2, 3]
         })

    df_2 = pd.DataFrame(
        {'formula_id': [1, 2, 3],
         'strategy': ['c_red', 'c_white', 'c_blue'],
         'numbers_2': [1, 2, 3]
         })

    def test_filter_numbers_as_strategy(self):
        match = "numbers"
        filtered = exclude_annotate(self.df, list(match), match)
        self.assertEqual(2, len(filtered.columns))
        self.assertEqual("strategy", filtered.columns[-1])
        self.assertNotIn(match, filtered.columns[0])

    def test_filter_colors_and_numbers_as_strategy(self):
        match = "numbers"
        exclude = [match, "colors"]
        filtered = exclude_annotate(self.df, exclude, match)
        self.assertEqual(1, len(filtered.columns))
        self.assertEqual("strategy", filtered.columns[-1])
        self.assertNotIn(match, filtered.columns[0])
        self.assertEqual("strategy", filtered.columns[0])

    def test_selecting_numbers2_as_metric(self):
        metric = "numbers_2"
        selected = select_metric(self.df_2, metric)
        self.assertEqual(4, len(selected.columns))
        self.assertEqual("value", selected.columns[-2])
        self.assertEqual("metric", selected.columns[-1])

    def test_splitting_by_strategies(self):
        strategies = {"numbers": "num", "colors": "col"}
        split = split_by_dictionary(self.df, strategies)
        self.assertEqual(2, len(split))
        self.assertEqual(3, len(split[0].columns))
        self.assertEqual(2, len(split[1].columns))
        self.assertEqual("strategy", split[0].columns[-1])
        self.assertEqual("strategy", split[1].columns[-1])
        self.assertNotIn("numbers_2", split[0].columns[0])
        self.assertEqual("num", split[0].iloc[0, -1])
        self.assertEqual("col", split[1].iloc[0, -1])

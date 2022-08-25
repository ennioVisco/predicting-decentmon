import unittest

import pandas as pd

from decmon.cleaner import rename, rename_list


class TestCleaner(unittest.TestCase):
    df = pd.DataFrame(
        {'numbers': [1, 2, 3],
         'colors': ['c_red', 'c_white', 'c_blue'],
         'numbers_2': [1, 2, 3]
         })

    def test_rename_column_works(self):
        renamed = rename(self.df, r"^numbers_(.*)", r"\1")
        self.assertEqual("2", renamed.columns[-1])

    def test_rename_multi_columns(self):
        renamed = rename_list(self.df, [r"(.*)2", r"col"], [r"\1 1", r"row"])
        self.assertEqual("numbers_ 1", renamed.columns[-1])
        self.assertEqual("rowors", renamed.columns[-2])

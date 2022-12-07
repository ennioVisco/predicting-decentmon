import unittest

import pandas as pd
from numpy import NaN

from decmon.learning import prepare_learning_sets, clean_df


class TestCleaner(unittest.TestCase):
    df = pd.DataFrame(
        {'id': [1, 2, 3],
         'colors': [0, 1, 1],
         })

    df2 = pd.DataFrame(
        {'id': [1, 2, 3],
         'colors': [0, 1, NaN],
         })

    def test_prepare_learning_sets(self):
        x_train, x_test, y_train, y_test = prepare_learning_sets(self.df, "id")
        self.assertEqual(2, len(x_train))
        self.assertEqual(1, len(x_test))
        self.assertEqual(2, len(y_train))
        self.assertEqual(1, len(y_test))

    def test_cleaning_df(self):
        cleaned = clean_df(self.df2, ["id"])
        self.assertEqual(1, len(cleaned.columns))
        self.assertEqual(3, len(cleaned))
        self.assertEqual(0, cleaned.iloc[0, 0])
        self.assertEqual(1, cleaned.iloc[1, 0])
        self.assertEqual(0, cleaned.iloc[2, 0])

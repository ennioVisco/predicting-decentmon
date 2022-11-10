from pandas import DataFrame

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import normalize


def prepare_learning_sets(df: DataFrame, target: str) \
        -> (DataFrame, DataFrame, DataFrame, DataFrame):
    y = df[target].values
    X = df.drop(target, axis=1)
    X = normalize(X)
    X_train, X_test, y_train, y_test = \
        train_test_split(X, y, test_size=0.3, random_state=0)
    return X_train, X_test, y_train, y_test


def clean_df(df: DataFrame, cols_to_drop: [str]) -> DataFrame:
    new_df = df.drop(cols_to_drop, axis=1)
    new_df = new_df.fillna(0)
    return new_df

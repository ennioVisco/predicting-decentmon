from pandas import DataFrame

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import normalize


def prepare_learning_sets(df: DataFrame, target: str) \
        -> (DataFrame, DataFrame, DataFrame, DataFrame):
    """
    Prepare training and testing sets for a given DataFrame and target column.
    :param df: the dataframe to split
    :param target: the target column
    :return: the training and testing sets
    """
    y = df[target].values
    X = df.drop(target, axis=1)
    X = normalize(X)
    X_train, X_test, y_train, y_test = \
        train_test_split(X, y, test_size=0.3, random_state=0)
    return X_train, X_test, y_train, y_test


def clean_df(df: DataFrame, cols_to_drop: [str]) -> DataFrame:
    """
    Drops the given columns from the dataframe and fills the NaN values with 0.
    :param df: the dataframe to clean
    :param cols_to_drop: the columns to drop
    :return: a cleaned copy of the original dataframe
    """
    new_df = df.drop(cols_to_drop, axis=1)
    new_df = new_df.fillna(0)
    return new_df

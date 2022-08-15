from pandas import DataFrame
from typing import List


def rename(df: DataFrame, find: str, replace: str, regex=True) -> DataFrame:
    """
    Returns a copy of the dataframe where the given column pattern is renamed
    :param df: source dataframe to copy
    :param find: keyword to match
    :param replace: replacement for the match
    :param regex: whether the pattern is a regular expression (default: true)
    :return: a copy of the original dataframe
    """
    new_df = df.copy()
    new_df.columns = new_df.columns.str.replace(find, replace, regex=regex)
    return new_df


def rename_list(df: DataFrame, find: List[str], replace: List[str]) \
        -> DataFrame:
    """
    Returns a copy of the dataframe where the given column patterns are renamed.
    The replacement is positional:
    the i-th pattern is replaced with the i-th string
    :param df: source dataframe to copy
    :param find: list of keywords to match
    :param replace: list of replacements for the match
    :return: a copy of the original dataframe
    """
    new_df = df.copy()
    elements = [e for e in range(0, len(find))]
    for i in elements:
        new_df = rename(new_df, find[i], replace[i])
    return new_df

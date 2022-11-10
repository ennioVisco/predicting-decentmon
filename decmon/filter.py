from pandas import DataFrame

from decmon.cleaner import rename, drop_columns


def exclude_annotate(df: DataFrame, exclude: list[str], annotate: str)\
        -> DataFrame:
    """
    Excludes the given columns from the dataframe and annotates the dataframe
    with an extra column having the given annotation.
    :param df: the dataframe to process
    :param exclude: the columns to exclude
    :param annotate: the annotation to add
    :return: a copy of the original dataframe
    """
    to_return = df.copy()
    for e in exclude:
        filtered = to_return.filter(regex=f"^{e}.*", axis=1)
        to_return = drop_columns(to_return, filtered.columns)

    to_return['strategy'] = annotate
    return to_return


def select_metric(df: DataFrame, metric: str) -> DataFrame:
    """
    Selects the given column metric to the pair of columns (metric, value)
    :param df: the dataframe having the current metric
    :param metric: the metric to extract
    :return: a copy of the original dataframe where the metric column
    is replaced with the pair (metric, value)
    """
    new_df = df[['formula_id', 'strategy', metric]].copy()
    new_df['metric'] = metric
    new_df = new_df.rename(columns={metric: "value"})
    return new_df


def split_by_dictionary(df: DataFrame, strategies: dict[str, str]) \
        -> list[DataFrame]:
    """
    Splits the dataframe by the given dictionary of strategies.
    :param df: the dataframe to split
    :param strategies: the dictionary of strategies
    :return: a list of dataframes, each one having the given strategy
    """
    ddf = []
    for key, name in strategies.items():
        others = {x: strategies[x] for x in strategies if x != key}
        other_keys = list(others.keys())
        local = rename(df, fr"^{key}_(.*)", r"\1")
        local = exclude_annotate(local, exclude=other_keys, annotate=name)
        ddf.append(local)
    return ddf

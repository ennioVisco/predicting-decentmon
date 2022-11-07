from pandas import DataFrame

from decmon.cleaner import rename


def exclude_annotate(data: DataFrame, exclude: list[str] | str,
                     annotate: str):
    to_return = data.copy()
    if isinstance(exclude, str):
        exclude = [exclude]

    for e in exclude:
        filtered = to_return.filter(regex=f"^{e}.*", axis=1)
        to_return = to_return.drop(filtered.columns, axis=1)

    to_return['strategy'] = annotate
    return to_return


def select_metric(df: DataFrame, metric: str):
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
    ddf = []
    for key, name in strategies.items():
        others = {x: strategies[x] for x in strategies if x != key}
        other_keys = list(others.keys())
        local = rename(df, fr"^{key}_(.*)", r"\1")
        local = exclude_annotate(local, exclude=other_keys, annotate=name)
        ddf.append(local)
    return ddf

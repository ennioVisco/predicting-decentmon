from typing import List, Union
import pandas as pd


def exclude_annotate(data: pd.DataFrame, exclude: Union[List[str], str],
                     annotate: str):
    to_return = data.copy()
    if isinstance(exclude, str):
        exclude = [exclude]

    for e in exclude:
        filtered = to_return.filter(regex=f"^{e}.*", axis=1)
        to_return = to_return.drop(filtered.columns, axis=1)

    to_return['strategy'] = annotate
    return to_return


def select_metric(df, metric):
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

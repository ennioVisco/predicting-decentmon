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

#    to_return.columns = to_return.columns.str.replace(prefix, "")

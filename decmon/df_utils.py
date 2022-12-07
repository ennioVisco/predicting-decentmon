from pandas import read_csv, DataFrame, concat

from decmon.constants import METRICS
from decmon.extractor import encode_ops
from decmon.filter import select_metric


def load_simulation_data(path: str) -> DataFrame:
    """
    Loads the simulation data from the given path.
    :param path: path to the simulation data
    :return: dataframe with simulation data
    """
    df = read_csv(path, sep='@')
    df.insert(0, 'formula_id', range(0, len(df)))
    df.columns = df.columns.str.strip()
    return df


def extract_ops(df: DataFrame) -> (DataFrame, DataFrame):
    """
    Extracts the operations from the given dataframe. This includes
    the encoded operations within the full expansion of the formula.
    :param df: dataframe to extract operations from
    :return: dataframe with fully expanded formula and encoded operations
    """
    df = df.copy()
    df["formula"] = df["formula"].map(encode_ops)

    return DataFrame(df["formula"].tolist())


def extract_metrics(df: DataFrame) -> DataFrame:
    """
    Extracts the metrics (as in decmon.constants.METRICS)
    from the given dataframe.
    :param: df: dataframe to extract metrics from
    :return: dataframe with extra metric-related columns
    """
    metrics_data = []
    for metric in METRICS.keys():
        metrics_data.append(select_metric(df, metric))

    merged_metrics = concat(metrics_data)
    return merged_metrics


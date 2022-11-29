from pandas import read_csv, DataFrame, concat
from ast import literal_eval

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


def col_gen(df, label):
    """
    Generates a set of columns for the given label and value.
    :param df: dataframe to generate columns for
    :param label: label of the column
    :return: dataframe with generated columns
    """
    props = literal_eval(df[label])
    for i in range(len(props)):
        df[f'{label}_{str(i + 1)}'] = props[i]
    return df


def map_ops(df: DataFrame) -> DataFrame:
    """
    Maps the operations to the given dataframe.
    :param df: dataframe to map operations to
    :return: dataframe with mapped operations
    """
    props = encode_ops(df['formula'])
    for i, p in enumerate(props):
        df[f'op_{i + 1}'] = p
    return df


def extract_ops(df: DataFrame) -> (DataFrame, DataFrame):
    """
    Extracts the operations from the given dataframe. This includes
    the encoded operations within the full expansion of the formula.
    :param df: dataframe to extract operations from
    :return: dataframe with fully expanded formula and encoded operations
    """
    # # def map_ops(x): return str(encode_ops(x['formula']))
    # full_expansion = DataFrame(df['formula'])
    # full_expansion.apply(map_ops, axis=1)
    #
    # df = Series(df['formula'])
    # props = encode_ops()
    #
    # # def generate_col(x): return col_gen(x, "total_ops_list")
    # # encoded_ops = full_expansion.apply(generate_col, axis=1)
    #
    # to_drop = ['formula']
    # encoded_ops = drop_columns(full_expansion, to_drop)
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


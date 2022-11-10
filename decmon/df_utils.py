from pandas import read_csv, DataFrame, concat
from ast import literal_eval

from decmon.cleaner import drop_columns
from decmon.constants import METRICS
from decmon.extractor import encode_ops, flatten_once, count_all_ops
from decmon.filter import select_metric


def load_simulation_data(path: str) -> DataFrame:
    df = read_csv(path, sep='@')
    df.insert(0, 'formula_id', range(0, len(df)))
    df.columns = df.columns.str.strip()
    return df


def col_gen(x, label):
    props = literal_eval(x[label])
    for i in range(len(props)):
        x[f'{label}_{str(i + 1)}'] = props[i]
    return x


def extract_ops(data: DataFrame) -> (DataFrame, DataFrame):
    def map_ops(x): return str(encode_ops(x['formula']))
    def map_ops2(x): return sum(flatten_once(count_all_ops(x['formula'])))
    full_expansion = DataFrame(data['formula'])
    full_expansion['total_ops_list'] = full_expansion.apply(map_ops, axis=1)
    full_expansion['total_ops'] = full_expansion.apply(map_ops2, axis=1)

    def generate_col(x): return col_gen(x, "total_ops_list")
    encoded_ops = full_expansion.apply(generate_col, axis=1)

    to_drop = ['total_ops_list', 'total_ops', 'formula']
    encoded_ops = drop_columns(encoded_ops, to_drop)

    return encoded_ops, full_expansion


def extract_metrics(df: DataFrame) -> DataFrame:
    """
    Extracts the metrics (as in decmon.constants.METRICS)
    from the given dataframe.

    :param: df: dataframe to extract metrics from
    :return: dataframe with extra metric-related columns
    """
    metrics_data = []
    for metric in METRICS:
        metrics_data.append(select_metric(df, metric))

    merged_metrics = concat(metrics_data)
    return merged_metrics

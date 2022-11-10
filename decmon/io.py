from pandas import read_csv, DataFrame


def load_simulation_data(path: str) -> DataFrame:
    df = read_csv(path, sep='@')
    df.insert(0, 'formula_id', range(0, len(df)))
    df.columns = df.columns.str.strip()
    return df

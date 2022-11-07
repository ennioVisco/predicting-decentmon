import pandas as pd

INPUT_DIR = "input"

STRATEGIES = {
    "cent": "orchestration",
    "decent": "migration",
    "odecent": "choreography"
}

METRICS = [
    "trace_len",
    "num_mess",
    "size_mess",
    "nb_progressions"
]


def load_simulation_data(path: str):
    df = pd.read_csv(path, sep='@')
    df.insert(0, 'formula_id', range(0, len(df)))
    df.columns = df.columns.str.strip()
    return df

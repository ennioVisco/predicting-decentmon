# Decentmon scripts
This repo is thought to provide information already by exploring it, although any of the notebook can be locally run and modified.

The notebooks can be run in two ways, via docker (unstable because of issues of jupyter with docker, see e.g. https://github.com/microsoft/vscode-jupyter/issues/8670) and via poetry (RECOMMENDED):

## Install via Docker (Not recommended)
To run them via docker, just run:
```sh
docker build -t dist-mon . 
```
And once done,
```sh
docker run -dp 8888:8888 --user root dist-mon
```
## Install via Poetry (Recommended)
To run them via poetry, follow these instructions (they require python 3.7+ in the running environment):

```sh
pip install poetry
```
And afterward:
```sh
poetry install
```
And finally:
# Run
```sh
poetry run jupyter notebook
```

# Open notebooks:
Whichever procedure you used, notebooks should be available at http://localhost:8888

## Extract data
Most of the simulation data is available in `input/3_5_7_9.zip`.

~~Extract the content in the same directory to run the scripts.~~

It has been pre-extracted to simplify the first run.

# Repository structure
The repository is organized as follows:

- `decmon` and `test` contain the code (and tests) that have been developed to process, organize and transform the data.
- `input` is the folder from which we will read traces
- `output` is where the output files will be generated (e.g. statistics pictures). It is already filled with the files generated from the run of the paper.
- `decent` contains the decentmon tool. It is not required to setup it to run the experiments, although the user interested in simulating new/alternative traces, can refer to https://github.com/ennioVisco/decent-tools for installation details, and customize the `run.py` file to automatically import the resulting traces in the current project.
- `formula_patterns_1/2.png` contain some aggregated stats about the formulae that have been generated for the experiments.

### Then a set of notebooks is available:
Note that all notebooks have paper-run information preloaded, although they can be re-run on demand.
- `full_data_*.ipynb` contain the data preprocessing for respectively systems of `3`, `5`, `7` and `9` nodes.
- `trace_encoding.ipynb` and `preparation.ipynb` encode and prepare the data for the learning process.
- `classification.ipynb` contains all the classification models trainings
- `regression_*.ipynb` contain the regression models trainings for respectively systems of `3`, `5`, `7` and `9` nodes, and for each metric.
- `regression_*_linear.ipynb` contain the comparison and plotting among the linear models for respectively systems of `3`, `5`, `7` and `9` nodes, and for each metric.

Please note that each `regression_*` file can require several hours to run!

# Misc

### Development

To run unit tests:
```shell
python -m unittest discover
```

Or with coverage:
```shell
coverage run -m unittest discover
```

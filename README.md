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
And afterwards:
```sh
poetry install
```
And finally:
# Run
```sh
jupyter notebook
```

# Open notebooks:
Whichever procedure you used, notebooks should be available at http://localhost:8888

## Extract data
Most of the simulation data is available in `input/3_5_7_9.zip`.
Extract the content in the same directory to run the scripts.

# Repository structure
The repository is organized as follows:

- `decmon` contains the code that has been developed to process, organize and transform the data.
- `input` is the folder from which we will read traces
- `output` is where the output files will be generated (e.g. statistics pictures). It is already filled with the files generated from the run of the paper.
- 

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

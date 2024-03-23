# We start from a Jupyter Notebook base image
FROM jupyter/base-notebook:4d70cf8da953

# We prepare the environment to be sure that Poetry is detected
ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH" \
    POETRY_PATH=/opt/poetry
ENV PATH="$POETRY_PATH/bin:$VENV_PATH/bin:$PATH"

# We copy the project files in the VM
WORKDIR /app
COPY . .

# We install the base dependencies for Python and OCaml
USER root
RUN apt-get update \
    && apt-get install -y build-essential \
    && apt-get install -y opam \
    && apt-get install -y camlp5 \
    && apt-get install -y xdot

# We set up OCaml
RUN opam init --compiler=4.14.0 --disable-sandboxing
RUN opam install -y dune batteries camlp5
ENV DUNE_CONFIG__GLOBAL_LOCK=disabled

# We build Decentmon
WORKDIR /app/decent
RUN opam exec -- dune build

# We go back to the python application for the final installation
COPY . .

# We install poetry and the required dependencies of the project
RUN pip install poetry==1.8.2
RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction --no-cache

# We expose the port to the user
EXPOSE 8888

# We run jupyter lab via Poetry
CMD poetry run jupyter lab --ip='*' --port=8888 --no-browser --allow-root --NotebookApp.token='' --NotebookApp.password=''


FROM jupyter/base-notebook:095717cb5793

WORKDIR /app

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

COPY . .

RUN conda config --set pip_interop_enabled True

RUN conda install --file requirements.txt

RUN pip install mgzip ipynb 

RUN conda update --all

CMD ["jupyter", "notebook", "--ip='*'", "--NotebookApp.token=''", "--NotebookApp.password=''", "--allow-root"]
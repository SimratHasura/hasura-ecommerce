# start by pulling the python image
# pg_config required for psycopg2, quick hack to go whole 3.9 image instead of slim
FROM python:3.9 as python-base

ENV POETRY_VERSION=1.4.2\
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH="/superrag" \
    VENV_PATH="/.venv" 

# Prepend poetry and venv to path
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"
ENV PYTHONPATH=PYSETUP_PATH

FROM python-base as builder-base
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
    curl \
    build-essential

# install poetry
RUN pip3 install poetry

# switch working directory
WORKDIR $PYSETUP_PATH
COPY . /superrag

RUN poetry config virtualenvs.create false
RUN poetry install --no-dev -vvv

EXPOSE 5000

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "5000"]
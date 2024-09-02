FROM python:3.12

WORKDIR /code

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_NO_INTERACTION=1

# to run poetry directly as soon as it's installed
ENV PATH="$POETRY_HOME/bin:$PATH"
# Add Poetry to PATH
ENV PATH="/root/.local/bin:${PATH}"
ENV PATH="/usr/bin:${PATH}"
ENV PATH="/opt/venv:${PATH}"


# install poetry
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && curl -sSL https://install.python-poetry.org | python3 -

COPY ./pyproject.toml ./poetry.lock /code/

RUN poetry install --no-interaction --no-ansi

CMD ["poetry","run","gunicorn", "main:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8080"]
FROM python:3.11-slim-buster

ARG ENV
ARG GUNICORN_LOG_LEVEL
ENV PYTHONUNBUFFERED=1
ENV POETRY_VERSION=1.4.2

RUN apt-get update && apt-get install -y gcc python-dev
RUN apt-get install -y libpq-dev postgresql-client

COPY ./components /app/components/
COPY ./docker /app/docker/
COPY ./db_migrations /app/db_migrations/
COPY ./alembic.ini /app/
COPY poetry.lock pyproject.toml README.md /app/

WORKDIR app

RUN pip install -U pip
RUN pip install "poetry==$POETRY_VERSION"
RUN poetry config virtualenvs.create false
RUN poetry install

EXPOSE 5000

CMD [ "/app/docker/entrypoints/entrypoint.sh" ]
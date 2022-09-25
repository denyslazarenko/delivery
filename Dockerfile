FROM python:3.9.1

ENV POETRY_HOME=/etc/poetry
ENV POETRY_VERSION=1.1.13
ENV POETRY_VIRTUALENVS_CREATE=false
ENV PATH="${POETRY_HOME}/bin:$PATH"
ENV PYTHONPATH "${PYTHONPATH}:/usr/src/app/"

RUN pip install --upgrade pip && \
    curl -sSL https://install.python-poetry.org | python3 -

WORKDIR /usr/src/app/

COPY ./pyproject.toml ./poetry.lock ./
RUN poetry install --no-root

COPY src src
COPY app.py app.py
COPY config.py config.py
COPY prod.env prod.env


EXPOSE 5001
CMD ["python3", "app.py"]
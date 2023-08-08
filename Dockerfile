FROM python:3.11.3-slim-bullseye

WORKDIR /app
COPY poetry.lock pyproject.toml ./

RUN python -m pip install --no-cache-dir poetry==1.5.1 \
    && poetry config virtualenvs.in-project true \
    && poetry install --no-interaction --no-ansi

COPY . .

CMD [".venv/bin/python", "./main.py"]
#CMD [".venv/bin/flet", "run", "-p", "8000", "-r", "-n", "-m", "configuration.run"]

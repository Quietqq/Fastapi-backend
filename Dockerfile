FROM python:3.11.4

RUN mkdir /app

WORKDIR /app


COPY /pyproject.toml .


RUN pip install poetry\
    && poetry config virtualenvs.create false\
    && poetry install

COPY . .


CMD alembic upgrade head\
    && gunicorn src.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000


# RUN /bin/bash -c "chmod -R 777 docker/*.sh"
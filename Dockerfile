FROM python:3.11.3-slim-buster

WORKDIR /usr/src/app

COPY Pipfile .
COPY Pipfile.lock .

RUN pip install pipenv requests&& \
    pipenv --bare install --system --ignore-pipfile --dev

COPY . .
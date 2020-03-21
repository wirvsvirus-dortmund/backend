# Backend [![Build Status](https://travis-ci.com/wirvsvirus-dortmund/backend.svg?branch=master)](https://travis-ci.com/wirvsvirus-dortmund/backend)

Backend for the shop status and appointment service using flask and sqlalchemy


## Getting started


This is a python project using [`poetry`](https://python-poetry.org/docs/basic-usage).

You'll need python ≥ 3.6.

1. Get poetry:
    ```
    $ python install [--user] poetry
    ```

1. Copy the env-template and fill in the config
    ```
    $ cp env-template .env
    ```

1. Install dependencies
    ```
    $ poetry install
    ```

1. Run database migrations
    ```
    $ poetry run flask db upgrade
    ```

1. Run the unit tests

    ```
    $ poetry run python -m pytest
    ```

1. Start app in debug mode
    ```
    FLASK_DEBUG=true poetry run flask run
    ```

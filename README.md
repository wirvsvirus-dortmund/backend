# Backend [![Build Status](https://travis-ci.com/wirvsvirus-dortmund/backend.svg?branch=master)](https://travis-ci.com/wirvsvirus-dortmund/backend)

Backend for the shop status and appointment service using flask and sqlalchemy


## Getting started


This is a python project using [`poetry`](https://python-poetry.org/docs/basic-usage).

You'll need python ≥ 3.6.

1. Get poetry:
    ```
    $ pip install [--user] poetry
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

1. You can add some random data to the database using
    ```
    $ poetry run python examples/fill_some_data.py
    ```

1. httpie is a great http cli, e.g. you can look at the customer data for a shop:
    ```
    http :5000/api/shops/1/customers
    ```

## Conflicts in poetry.lock

When poetry.lock has conflicts, don't bother resolving them by hand.
Delete the file and recreate it by running `poetry install`.

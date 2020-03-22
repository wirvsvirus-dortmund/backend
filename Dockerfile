# create a build stage
# see https://stackoverflow.com/a/54763270/3838691
FROM python:3.8-slim AS BUILDER

# we always want to serve the member_database app
ENV FLASK_APP=backend \
	PORT=5000 \
	PIP_NO_CACHE_DIR=1 \
	PIP_DISABLE_PIP_VERSION_CHECK=1 \
	PYTHONUNBUFFERED=1

# everything should run as the memberdb user (not root, best practice)
RUN useradd --system --user-group supermarkt

# we need the pg_dump executable for auto backups
RUN apt-get update && apt-get install -y  libpq-dev gcc postgresql-client \
    && rm -rf /var/lib/apt/lists/*

RUN pip install poetry==1.0.5
WORKDIR /home/supermarkt/

# this will be our startup script
COPY run.sh .

# migrations are needed at startup
COPY migrations migrations

# copy relevant files
COPY pyproject.toml poetry.lock ./

# install production dependencies
# this is our production server
# on top, for production we use postgresql, which needs psycopg2 and
# pg_config
# this will create a wheel file that contains all dependencies
RUN poetry config virtualenvs.create false \
	&& poetry install -E deploy --no-dev

COPY backend ./backend

# switch to our production user
USER supermarkt
CMD ./run.sh

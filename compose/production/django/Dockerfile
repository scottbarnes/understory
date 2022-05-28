FROM python:3.9-slim-buster as client-builder

ARG APP_HOME=/code
WORKDIR ${APP_HOME}

# COPY ./package.json ${APP_HOME}
# RUN npm install && npm cache clean --force
COPY . ${APP_HOME}
# RUN npm run build

# ARG PYTHON_VERSION=3.9-slim-buster

# define an alias for the specfic python version used in this file.
FROM python:3.9-slim-buster as python

# Python build stage
FROM python as python-build-stage

ARG BUILD_ENVIRONMENT=production

# Install apt packages
RUN apt-get update && apt-get install --no-install-recommends -y \
  # dependencies for building Python packages
  build-essential \
  git \
  # psycopg2 dependencies
  libpq-dev

# Requirements are installed here to ensure they will be cached.
COPY ./requirements .

# Create Python Dependency and Sub-Dependency Wheels.
RUN pip wheel --wheel-dir /usr/src/code/wheels  \
  -r ${BUILD_ENVIRONMENT}.txt


# Python 'run' stage
FROM python as python-run-stage

ARG BUILD_ENVIRONMENT=production
ARG APP_HOME=/code

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV BUILD_ENV ${BUILD_ENVIRONMENT}

WORKDIR ${APP_HOME}

RUN addgroup --system django \
    && adduser --system --ingroup django django


# Install required system dependencies
RUN apt-get update && apt-get install --no-install-recommends -y \
  # psycopg2 dependencies
  libpq-dev \
  # Translations dependencies
  gettext \
  # cleaning up unused files
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

# All absolute dir copies ignore workdir instruction. All relative dir copies are wrt to the workdir instruction
# copy python dependency wheels from python-build-stage
COPY --from=python-build-stage /usr/src/code/wheels  /wheels/

# use wheels to install python dependencies
RUN pip install --no-cache-dir --no-index --find-links=/wheels/ /wheels/* \
  && rm -rf /wheels/


COPY --chown=django:django ./compose/production/django/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint


COPY --chown=django:django ./compose/production/django/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start

# copy application code to WORKDIR
COPY --from=client-builder --chown=django:django ${APP_HOME} ${APP_HOME}


# make django owner of the WORKDIR directory as well.
RUN chown django:django ${APP_HOME}

USER django

ENTRYPOINT ["/entrypoint"]

# # Use an official Python runtime as a parent image
# FROM python:3.9-alpine
# LABEL maintainer="hello@wagtail.io"

# # Set environment varibles
# ENV PYTHONUNBUFFERED 1
# # ENV DJANGO_ENV dev

# # Add user that will be used in the container.
# # RUN useradd wagtail
# RUN addgroup -S wagtail && adduser -S wagtail -G wagtail

# # # Install system packages required by Wagtail and Django.
# RUN apk update && \
#     apk add \
#     libpq-dev \
#     mysql-client \
#     libjpeg-turbo-dev \
#     zlib-dev \
#     libwebp-dev && \
#     apk add --virtual build-dependencies \
#     build-base \
#     git

# # # Install system packages required by Wagtail and Django.
# # RUN apt-get update --yes --quiet && apt-get install --yes --quiet --no-install-recommends \
# #     build-essential \
# #     libpq-dev \
# #     default-libmysqlclient-dev \
# #     git \
# #     libjpeg62-turbo-dev \
# #     zlib1g-dev \
# #     libwebp-dev \
# #  && rm -rf /var/lib/apt/lists/*

# # Install the application server.
# RUN pip install "gunicorn==20.0.4"

# # Install the project requirements.
# COPY requirements.txt /
# RUN pip install -r /requirements.txt

# RUN apk del build-dependencies

# # Use /code folder as a directory where the source code is stored.
# WORKDIR /code

# # Set this directory to be owned by the "wagtail" user.
# RUN chown wagtail:wagtail /code

# # Copy the source code of the project into the container.
# COPY --chown=wagtail:wagtail . .
# RUN sed -i 's/\r$//g' ./start && chmod +x ./start

# # Use user "wagtail" to run the build commands below and the server itself.
# USER wagtail

# # Collect static files.
# RUN python manage.py collectstatic --noinput --clear

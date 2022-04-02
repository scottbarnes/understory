# Use an official Python runtime as a parent image
FROM python:3.9-alpine
LABEL maintainer="hello@wagtail.io"

# Set environment varibles
ENV PYTHONUNBUFFERED 1
# ENV DJANGO_ENV dev

# Add user that will be used in the container.
# RUN useradd wagtail
RUN addgroup -S wagtail && adduser -S wagtail -G wagtail

# # Install system packages required by Wagtail and Django.
RUN apk update && \
    apk add \
    libpq-dev \
    mysql-client \
    libjpeg-turbo-dev \
    zlib-dev \
    libwebp-dev && \
    apk add --virtual build-dependencies \
    build-base \
    git

# # Install system packages required by Wagtail and Django.
# RUN apt-get update --yes --quiet && apt-get install --yes --quiet --no-install-recommends \
#     build-essential \
#     libpq-dev \
#     default-libmysqlclient-dev \
#     git \
#     libjpeg62-turbo-dev \
#     zlib1g-dev \
#     libwebp-dev \
#  && rm -rf /var/lib/apt/lists/*

# Install the application server.
RUN pip install "gunicorn==20.0.4"

# Install the project requirements.
COPY requirements.txt /
RUN pip install -r /requirements.txt

RUN apk del build-dependencies

# Use /code folder as a directory where the source code is stored.
WORKDIR /code

# Set this directory to be owned by the "wagtail" user.
RUN chown wagtail:wagtail /code

# Copy the source code of the project into the container.
COPY --chown=wagtail:wagtail . .
RUN sed -i 's/\r$//g' ./start && chmod +x ./start

# Use user "wagtail" to run the build commands below and the server itself.
USER wagtail

# Collect static files.
RUN python manage.py collectstatic --noinput --clear

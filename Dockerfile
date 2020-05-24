# Use an official Python runtime as a parent image
FROM python:3.7
LABEL maintainer="hello@wagtail.io"

# Set environment varibles
ENV PYTHONUNBUFFERED 1
ENV DJANGO_ENV dev

COPY ./requirements.txt /code/requirements.txt
RUN pip install --upgrade pip
# Install any needed packages specified in requirements.txt
RUN pip install -r /code/requirements.txt
RUN pip install gunicorn

# Copy the current directory contents into the container at /code/
COPY . /code/
COPY ./static/ /code/understory/static/
RUN sed -i 's/\r$//g' /code/start
RUN chmod +x /code/start

# Set the working directory to /code/
WORKDIR /code/

RUN python manage.py migrate

RUN useradd wagtail
RUN chown -R wagtail /code
USER wagtail

# Handle from docker-compose.yml and 'start'
# EXPOSE 8000
# CMD exec gunicorn understory.wsgi:application --bind 0.0.0.0:8004 --workers 3

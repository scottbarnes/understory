#!/bin/sh

echo understory=production >> .env
echo DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE >> .env
echo DJANGO_SECRET_KEY=$DJANGO_SECRET_KEY >> .env
echo DJANGO_ALLOWED_HOSTS=$DJANGO_ALLOWED_HOSTS >> .env

echo db_name=$db_name >> .env
echo db_user=$db_user >> .env
echo db_pass=$db_pass >> .env
echo db_host=$db_host >> .env
echo db_port=$db_port >> .env

echo POSTGRES_DB=$POSTGRES_DB >> .env
echo POSTGRES_USER=$POSTGRES_USER >> .env
echo POSTGRES_PASSWORD=$POSTGRES_PASSWORD >> .env
echo POSTGRES_HOST=$POSTGRES_HOST >> .env
echo POSTGRES_PORT=$POSTGRES_PORT >> .env

# django-slack
echo DJANGO_SLACK_TOKEN=$DJANGO_SLACK_TOKEN >> .env
echo DJANGO_SLACK_CHANNEL=$DJANGO_SLACK_CHANNEL >> .env

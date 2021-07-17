#!/bin/sh

echo understory=production >> .django
echo DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE >> .django
echo DJANGO_SECRET_KEY=$DJANGO_SECRET_KEY >> .django
echo DJANGO_ALLOWED_HOSTS=$DJANGO_ALLOWED_HOSTS >> .django

echo db_name=$db_name >> .django
echo db_user=$db_user >> .django
echo db_pass=$db_pass >> .django
echo db_host=$db_host >> .django
echo db_port=$db_port >> .django

echo POSTGRES_DB=$POSTGRES_DB >> .django
echo POSTGRES_USER=$POSTGRES_USER >> .django
echo POSTGRES_PASSWORD=$POSTGRES_PASSWORD >> .django
echo POSTGRES_HOST=$POSTGRES_HOST >> .django
echo POSTGRES_PORT=$POSTGRES_PORT >> .django

# django-slack
echo DJANGO_SLACK_TOKEN=$DJANGO_SLACK_TOKEN >> .django
echo DJANGO_SLACK_CHANNEL=$DJANGO_SLACK_CHANNEL >> .django

echo DJANGO_SECRET_KEY=$DJANGO_SECRET_KEY >> .envs/.production/.django
echo DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE >> .envs/.production/.django
echo DJANGO_SLACK_CHANNEL=$DJANGO_SLACK_CHANNEL >> .envs/.production/.django
echo DJANGO_SLACK_TOKEN=$DJANGO_SLACK_TOKEN >> .envs/.production/.django
echo DJANGO_VERSION=$DJANGO_VERSION >> .env
echo POSTGRES_DB=$POSTGRES_DB >> .envs/.production/.postgres
echo POSTGRES_HOST=$POSTGRES_HOST >> .envs/.production/.postgres
echo POSTGRES_PASSWORD=$POSTGRES_PASSWORD >> .envs/.production/.postgres
echo POSTGRES_PORT=$POSTGRES_PORT >> .envs/.production/.postgres
echo POSTGRES_USER=$POSTGRES_USER >> .envs/.production/.postgres
echo TEST_ENV=$TEST_ENV >> .envs/.production/.django
# hostname:port:database:username:password
echo $POSTGRES_HOST:$POSTGRES_PORT:$POSTGRES_DB:$POSTGRES_USER: >> .pgpass

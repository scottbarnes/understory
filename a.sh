#!/bin/bash

set -e
set -u
set -o pipefail
set -x

docker-compose -f production.yml exec django python manage.py test

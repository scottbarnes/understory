from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'xi62o-virfe&r-i=9*b&oq3)(#jn)-vrod^an5^_pfx&wp_n$='

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ['*']

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Search
WAGTAILSEARCH_BACKENDS = {
    'default': {
        'BACKEND': 'wagtail.search.backends.elasticsearch7',
        'URLS': ['http://localhost:9200'],
        'INDEX': 'wagtail',
        'TIMEOUT': 5,
        'OPTIONS': {},
        'INDEX_SETTINGS': {},
        'AUTO_UPDATE': True,
    }
}

# DATABASES
# ------------------------------------------------------------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env('db_name'),
        'USER': env('db_user'),
        'PASSWORD': env('db_pass'),
        'HOST': env('db_host'),
        'PORT': env('db_port'),
    }
}



try:
    from .local import *
except ImportError:
    pass

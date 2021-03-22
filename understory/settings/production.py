from .base import *

DEBUG = False

try:
    from .local import *
except ImportError:
    pass

# Read the environment variables
environ.Env.read_env()

# Environment variables
SECRET_KEY = env('DJANGO_SECRET_KEY', default='aVtheUot32d-_&<>PBT<R')
#ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default=["understory-staging.fishcracker.net"])
ALLOWED_HOSTS = ['understory-staging.fishcracker.net', 'localhost', '.fishcracker.net']


# Search
WAGTAILSEARCH_BACKENDS = {
    'default': {
        'BACKEND': 'wagtail.search.backends.elasticsearch7',
        'URLS': ['http://elasticsearch:9200'],
        'INDEX': 'wagtail',
        'TIMEOUT': 5,
        'OPTIONS': {},
        'INDEX_SETTINGS': {},
        'AUTO_UPDATE': True,
    }
}

# Logging
LOGGING = {
	'version': 1,
	'disable_existing_loggers': False,
	'filters': {
		'require_debug_false': {
			'()': 'django.utils.log.RequireDebugFalse',
		},
		'require_debug_true': {
			'()': 'django.utils.log.RequireDebugTrue',
		},
	},
	'formatters': {
		'django.server': {
			'()': 'django.utils.log.ServerFormatter',
			'format': '[%(server_time)s] %(message)s',
		}
	},
	'handlers': {
		'console': {
			'level': 'INFO',
			'filters': ['require_debug_true'],
			'class': 'logging.StreamHandler',
		},
		'console_debug_false': {
			'level': 'ERROR',
			'filters': ['require_debug_false'],
			'class': 'logging.StreamHandler',
		},
		'django.server': {
			'level': 'INFO',
			'class': 'logging.StreamHandler',
			'formatter': 'django.server',
		},
	},
	'loggers': {
		'django': {
			'handlers': ['console', 'console_debug_false'],
			'level': 'INFO',
		},
		'django.server': {
			'handlers': ['django.server'],
			'level': 'INFO',
			'propagate': False,
		}
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

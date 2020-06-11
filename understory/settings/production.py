from .base import *

DEBUG = False

try:
    from .local import *
except ImportError:
    pass

# Environment variables
SECRET_KEY = env('DJANGO_SECRET_KEY')
ALLOWED_HOSTS = env('DJANGO_ALLOWED_HOSTS')

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

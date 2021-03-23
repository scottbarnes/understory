""" Context processor to add settings.DEBUG to the context. """
from django.conf import settings


def debug(request):
    """
    Take a request and return the value you want as a dictionary.
    Multiple values okay.
    """
    return {'DEBUG': settings.DEBUG}

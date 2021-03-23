""" Context processor to add settings.DEBUG to the context. """
from django.conf import settings
from django.template.loader import render_to_string


def debug(request):
    """
    Take a request and return the value you want as a dictionary.
    Multiple values okay.
    """
    return {'DEBUG': settings.DEBUG}


def analytics(request):
    """ Return a Google Analytics key """
    return {'GOOGLE_ANALYTICS_CODE': settings.GOOGLE_ANALYTICS_CODE}

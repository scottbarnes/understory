from django.db import models

class LanguageField(models.CharField):
    """
    LanguageField overwrites get_prep_value to enforce Title Case within
    the field.
    See https://stackoverflow.com/a/49181581
    See also: https://docs.djangoproject.com/en/4.0/ref/models/fields/#django.db.models.Field.get_prep_value
    """
    def __init__(self, *args, **kwargs):
        super(LanguageField, self).__init__(*args, **kwargs)

    def get_prep_value(self, value):
        return str(value).title()

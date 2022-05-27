""" Template tags for the footer. """

from django import template
from wagtail.templatetags.wagtailcore_tags import pageurl
from home.models import Copyright, PrivacyPolicy, TermsOfUse, Subscribe

register = template.Library()


# Copyright snippet
@register.simple_tag()
def copyright_text():
    """ Copyright text for the footer. There should only ever be one object. """
    if Copyright.objects.all().exists():
        return Copyright.objects.first()


# Privacy policy snippet
# @register.simple_tag()
# def privacy_policy():
#     """ Returns the privacy policy text and slug for the footer. There should only ever be one. """
#     return PrivacyPolicy.objects.first()
@register.filter()
def privacy_policy(field):
    """ Take an django filter variable (here, a model field name) and get that attribute of the
    first PrivacyPolicy object (there should only be one). This way it's possible in the
    Django template to have {{ 'field_name'|privacy_policy }} to get the text and slug
    fields. """
    if PrivacyPolicy.objects.all().exists():
        o = PrivacyPolicy.objects.first()
        result = getattr(o, field)
        if field == 'slug':
            """ This seemed the easiest way to generate the url as slugurl was messing up 
            on {% slugurl '{{ 'variable'|function }}' %}. """
            slug = o.slug
            if slug:
                return f'/{slug}'
        return result


# Terms of use snippet
@register.filter()
def terms_of_use(field):
    """ Takes Django filter variable and returns the corresponding fields. See note
     for privacy_policy. """
    if TermsOfUse.objects.all().exists():
        o = TermsOfUse.objects.first()
        result = getattr(o, field)
        if field == 'slug':
            # See comment for privacy_policy()
            slug = o.slug
            if slug:
                return f'/{slug}'
        return result


# 'Click here to subscribe' snippet
@register.filter()
def subscribe_text(field):
    """ Returns the text and url for the 'click here to subscribe' link. There should
    only ever be one. """
    if Subscribe.objects.all().exists():
        o = Subscribe.objects.first()
        result = getattr(o, field)
        if field == 'url':
            # See comment for privacy_policy()
            url = o.url
            if url:
                return url
        return result

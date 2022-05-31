from django import template
from django.utils.html import escape, mark_safe

register = template.Library()

# @register.simple_tag
@register.simple_tag()
def link_translations(iterable):
    """
    Output a list of HTML links to each translations of an article, excluding
    itself, with proper formatting for grammar.
    """
    output = ""
    count = len(iterable)

    if count == 1:
        output += f'<a href="{escape(iterable[0].get_url())}">{escape(iterable[0].language)}</a>'
    elif count == 2:
        output += f'<a href="{escape(iterable[0].get_url())}">{escape(iterable[0].language)}</a>'
        output += ' and '
        output += f'<a href="{escape(iterable[1].get_url())}">{escape(iterable[1].language)}</a>'
    else:
        for item in iterable:
            if item == iterable[-1]:
                output += 'and '
                output += f'<a href="{escape(item.get_url())}">{escape(item.language)}</a>'
            else:
                output += f'<a href="{escape(item.get_url())}">{escape(item.language)}</a>, ' # comma

    return mark_safe(output)

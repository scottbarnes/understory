def parse_search_fields(l: list) -> list:
    """
    NOTE: NOT CURRENTLY USED.

    Take a list, parse out unwanted fields (e.g. 'title'), and return it.
    
    By default, Wagtail's search_fields includes title fields. For search
    results this is undesireable because (1) making the field 'safe' renders
    the HTML, which may not be wanted, and (2) without 'safe' the HTML tags
    show up.

    This utility function filters out unwanted fields. Desired fields/methods,
    such as a custom method on the model that deals with HTML in title fields,
    can be added in the specific model inhereting from Page.

    See
    https://docs.wagtail.org/en/v2.16.2/topics/search/indexing.html#wagtailsearch-indexing-fields
    for more.
    """
    return [x for x in l if not x.field_name == 'title']

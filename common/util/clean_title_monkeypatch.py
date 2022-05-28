from wagtail.models import Page

def clean_title(self) -> str:
    """
    Remove <br /> from titles and return the result.
    """
    title = str(self.title)
    return ' '.join(title.split("<br />"))

Page.clean_title = clean_title

def clean_titler(Page):
    """
    Monkeypatch all instances of Page (including subclassed instances) to
    include the clean_title method.
    """
    Page.clean_title = clean_title
    return Page

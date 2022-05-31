from wagtail.core.models import Page
from django.db.models.query import QuerySet

def clean_title(self) -> str:
    """
    Remove <br /> from titles and return the result.
    """
    title = str(self.title)
    return ' '.join(title.split("<br />"))


def get_all_translations(self) -> list:
    """
    get_all_translations returns a list containing relevant translations
    for an article. If run from the English article, it returns a list of
    all the other languages in which the article is available. If run from on
    of the non-English translations, it returns a list with all other
    translations, excluding the one from which it was run, and including
    English. E.g., if an article is available in English, French, and Spanish,
    running .get_all_translations() on the English article would return a list
    with the French and Spanish articles, and if run from the Spanish article,
    it would return a QS of the English and French articles.
    """

    # Return an empty list if the requisite attributes are missing.
    if not hasattr(self, 'associated_English_article') \
       or not hasattr(self, 'translations'):
        return []

    # For English articles (i.e. no associated English article, because the
    # article itself is in English)
    if not self.associated_English_article:
        return list(self.translations.all().order_by('language'))

    def lang_sorter(article) -> str:
        """ Helper function for list.sort() to sort languages by name. """
        return article.language

    # When an article isn't English, get the associated English article, then
    # get all *other* translations of that article (excluding itself). Then append
    # the English article to the list.
    english_article = self.associated_English_article
    translations = list(english_article.translations.exclude(id=self.id))
    translations.append(english_article)
    translations.sort(key=lang_sorter)
    return translations



Page.clean_title = clean_title
Page.get_all_translations = get_all_translations


def monkey_patcher(Page):
    """
    Monkeypatch all instances of Page (including subclassed instances) to
    include the clean_title method.
    """
    Page.clean_title = clean_title
    Page.get_all_translations = get_all_translations
    return Page

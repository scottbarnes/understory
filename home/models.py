from django.db import models

from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel


class HomePage(Page):
    """ The home page. """
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('body', classname='full'),
    ]

    def get_context(self, request):
        """
        Modify the QuerySet to return the three most recent published Articles and Issues.
        """
        # Avoid circular imports.
        from article.models import ArticlePage
        from issue.models import IssuePage

        # Add the last three Articles and Issues to the context.
        context = super().get_context(request)
        articlepages = ArticlePage.objects.live().order_by('-first_published_at')[:3]
        articlepages = reversed(articlepages)
        context['articlepages'] = articlepages
        issuepages = IssuePage.objects.live().order_by('-first_published_at')[:3]
        issuepages = reversed(issuepages)
        context['issuepages'] = issuepages

        return context


class AboutPage(Page):
    """ The About page. """
    body = RichTextField(blank=True)
    content_panels = Page.content_panels + [
        FieldPanel('body', classname='full'),
    ]


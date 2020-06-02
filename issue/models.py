""" understory/issue/models.py """
from django.db import models

from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel


class IssueIndexPage(Page):
    """
    Main issue index page.
    Found at /issues
    """
    intro = RichTextField(blank=True)

    def get_context(self, request):
        """
        Modify QuerySet to return, in reverse chronological order, published issues.
        """
        context = super().get_context(request)
        issuepages = self.get_children().live().public().order_by('-first_published_at')
        context['issuepages'] = issuepages
        return context

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname='full'),
    ]


class IssuePage(Page):
    """
    Issue page model.
    Found at /issues/<issue>
    """
    date = models.DateField('Post date')
    intro = models.CharField(max_length=255)
    body = RichTextField(blank=True)
    # Todo add tags?

    def get_context(self, request):
        """
        Modify QuerySet to return only published articles within the issue.
        """
        from article.models import ArticlePage  # Avoid circular import.
        context = super().get_context(request)
        # articlepages = self.articles.live()  # Why is PyCharm flagging this?
        articlepages = ArticlePage.objects.filter(issue__id=self.id).live().public()
        context['articlepages'] = articlepages
        return context

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('date')
        ], heading='Issue information'),
        FieldPanel('intro'),
        FieldPanel('body'),
        InlinePanel('articles', label='Issue articles'),
    ]

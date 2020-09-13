""" understory/issue/models.py """
from django.db import models

from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel, PageChooserPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index


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

    subpage_types = [
        'issue.IssuePage',
    ]

    parent_page_type = [
        'wagtailcore.page',
    ]

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
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Landscape only; horizontal width between 1000px and 3000px.'
    )
    body = RichTextField(blank=True)
    # Todo add tags?

    def get_context(self, request):
        """
        Modify QuerySet to return only published articles within the issue.
        """
        from article.models import ArticlePage  # Avoid circular import.
        context = super().get_context(request)
        # articlepages = self.articles.live()  # Why is PyCharm flagging this?
        # For each issue, include articles that are associated with this issue ID, are public, and live. And in English.
        # articlepages = ArticlePage.objects.filter(issue__id=self.id).live().public()
        articlepages = ArticlePage.objects.filter(issue__id=self.id).live().public()
        context['articlepages'] = articlepages
        return context

    search_fields = Page.search_fields + [
        # index.SearchField('title'),  # This is redundant and causes an error.
        index.SearchField('body'),
        index.SearchField('intro'),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('date')
        ], heading='Issue information'),
        FieldPanel('intro'),
        ImageChooserPanel('image'),
        FieldPanel('body'),
        # InlinePanel('articles', label='Issue articles'),
    ]


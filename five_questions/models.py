# Create your models here.
""" understory/five_questions/models.py. """
from django.db import models
from django.shortcuts import render
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel, StreamFieldPanel
from wagtail.core import blocks
from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField, StreamField
from wagtail.images.blocks import ImageChooserBlock
from wagtail.embeds.blocks import EmbedBlock
from wagtail.images.models import Image
from wagtail.images.edit_handlers import ImageChooserPanel
from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.search import index
# from article.models import Author

BYLINE_CHOICES = (
    ('name', 'Name'),
    ('email', 'Email'),
    ('twitter', 'Twitter'),
    ('website', 'Website'),
)

ARTICLE_STATUS = (
    ('not_reviewed', 'Not reviewed'),
    ('review_in_progress', 'In progress'),
    ('review_complete', 'Review complete'),
)


class FiveQuestionsTagPage(TaggedItemBase):
    """
    Support for tagging individual resources.
    """
    content_object = ParentalKey(
        'FiveQuestionsPage',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )


# FiveQuestionsAuthororderable needs to go in article/models.py b/c of circular imports.

class FiveQuestionsIndexPage(Page):
    """
    The main Five Questions index page model.
    Location: /five-questions
    """
    intro = RichTextField(blank=True)

    def get_context(self, request):
        """
        Modify QuerySet to return posts in reverse chronological order and only return five_questionss
        that are published.
        """
        context = super().get_context(request)
        five_questionspages = self.get_children().live().public().order_by('-first_published_at')
        context['five_questionspages'] = five_questionspages
        return context

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname='full')
    ]

    subpage_types = [
        'five_questions.FiveQuestionsPage',
    ]

    parent_page_type = [
        'wagtailcore.page',
    ]


class FiveQuestionsPage(Page):
    """
    FiveQuestions page model. Formed from form input from FiveQuestionsSubmitPage and FiveQuestionsSubmitForm.
    Location: /five-questions/<five_questions-slug>
    """

    lead_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    lead_image_text = models.CharField(max_length=255, blank=True, null=True)
    body = StreamField([
        ('heading', blocks.CharBlock(classname="full title")),
        ('paragraph', blocks.RichTextBlock()),
        ('quote', blocks.BlockQuoteBlock()),
        ('image', ImageChooserBlock()),
        ('image_text', blocks.RichTextBlock()),
        ('embeded_item', blocks.RawHTMLBlock()),
    ])
    # Not displayed on the submission form.
    tags = ClusterTaggableManager(through=FiveQuestionsTagPage, blank=True)
    status = models.CharField(max_length=255, default='not_reviewed', choices=ARTICLE_STATUS)
    date = models.DateField('Post date', null=True, blank=True)
    intro = RichTextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # https://stackoverflow.com/questions/40554215/wagtail-filter-results-of-an-inlinepanel-foreignkey
    associated_English_five_questions = models.ForeignKey('self', on_delete=models.SET_NULL,
                                                          null=True, blank=True,
                                                          related_name='translations')
    language = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.title

    search_fields = Page.search_fields + [
        # index.SearchField('title'),  # This is redundant and causes an error.
        index.SearchField('body'),
        # index.SearchField('authors'),
        # index.SearchField('email'),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            InlinePanel("authors", label="Author", min_num=1, max_num=10)
            # FieldPanel('name'),
            # FieldPanel('email'),
            # FieldPanel('twitter'),
            # FieldPanel('website'),
        ], heading='Author(s)'),
        MultiFieldPanel([
            ImageChooserPanel('lead_image'),
            FieldPanel('lead_image_text'),
        ], heading='Lead'),
        FieldPanel('tags'),
        StreamFieldPanel('body'),
        MultiFieldPanel([
            FieldPanel('date'),
            FieldPanel('status'),
            FieldPanel('language'),
            FieldPanel('associated_English_five_questions'),
        ], heading='Editorial information'),
    ]


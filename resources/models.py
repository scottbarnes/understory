""" understory/resources/models.py. This is plural because 'resource' was a django conflict. """
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
from article.models import Author
from wagtail.snippets.models import register_snippet


class ResourceIndexPage(Page):
    """
    The main resource index page model.
    Location: /resources
    """
    intro = RichTextField(blank=True)

    def get_context(self, request):
        """
        Modify QuerySet to return resources in reverse chronological order and only return
        resources that are published.
        """
        context = super().get_context(request)
        resourcepages = self.get_children().live().public().order_by('-first_published_at')
        context['resourcepages'] = resourcepages
        return context

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname='full')
    ]

    subpage_types = [
        'resources.ResourcePage',
    ]

    parent_page_type = [
        'wagtailcore.page',
    ]


class ResourcePage(Page):
    """
    Resource page model.
    Location: /resources/<resources-slug>
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
    date = models.DateField('Post date', null=True, blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            ImageChooserPanel('lead_image'),
            FieldPanel('lead_image_text'),
        ], heading='Lead'),
        StreamFieldPanel('body')
    ]

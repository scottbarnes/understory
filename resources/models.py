""" understory/resources/models.py. This is plural because 'resource' was a django conflict. """
from django.db import models
from django.shortcuts import render
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel, FieldPanel
from wagtail import blocks
from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField, StreamField
from wagtail.images.blocks import ImageChooserBlock
from wagtail.embeds.blocks import EmbedBlock
from wagtail.images.models import Image
from wagtail.images.edit_handlers import FieldPanel
from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase
from wagtail.snippets.edit_handlers import FieldPanel
from wagtail.search import index
from article.models import Author, IMAGE_FORMATTING_CHOICES
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


# The clean_title method is monkeypatched via
# commun/util/clean_title_monkeypatch.py and FiveQuestionsPage
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
    lead_image_text = models.CharField(max_length=255, blank=True, null=True)  # Remove post migration
    lead_image_caption = models.CharField(max_length=255, blank=True, null=True)
    lead_image_alt_text = models.TextField(
        blank=True, null=True,
        help_text='Specify the alt text to improve site accessibility. This should be '
                  ' descriptive of the image and not merely a recitation of the caption'
                  ' text. Nor should it be duplicative of information in the caption.'
                  ' But it should be pithy. Perhaps no more than 125 characters.'
                  ' See best practices at https://axesslab.com/alt-texts/.'
    )
    lead_image_formatting_options = models.CharField(
        choices=IMAGE_FORMATTING_CHOICES,
        default='100_PERCENT_WIDTH',
        max_length=255,
        help_text='Select the formatting rules that apply this image. By default, images'
                  ' will span 100% of the width of the text column. Selecting 50% would'
                  ' render the image so that the width occupied 50% of the text column.'
                  ' Aspect ratios will be preserved. For a somewhat technical explanation'
                  ' of how images work in Wagtail, see https://docs.wagtail.io/en/v2.12.3/topics/images.html'
    )
    body = StreamField([
        ('heading', blocks.CharBlock(classname="full title")),
        ('paragraph', blocks.RichTextBlock(features=['redact', 'h1', 'h2',
                                                     'h3', 'h4',
                                                     'h5', 'h6', 'bold',
                                                     'italic', 'ol', 'ul',
                                                     'hr', 'embed', 'link',
                                                     'document-link', 'image',
                                                    'code', 'superscript',
                                                     'subscript',
                                                     'strikethrough',
                                                     'blockquote'])),
        ('quote', blocks.BlockQuoteBlock()),
        ('image', ImageChooserBlock()),
        ('image_with_alt_text', blocks.StructBlock([
            ('image', ImageChooserBlock()),
            ('caption_text', blocks.RichTextBlock(required=False)),
            ('alt_text', blocks.TextBlock(
                help_text='Specify the alt text to improve site accessibility. This should be '
                          ' descriptive of the image and not merely a recitation of the caption'
                          ' text. Nor should it be duplicative of information in the caption.'
                          ' But it should be pithy. Perhaps no more than 125 characters.'
                          ' See best practices at https://axesslab.com/alt-texts/.'
            )),
            ('formatting_options', blocks.ChoiceBlock(
                required=False,
                choices=IMAGE_FORMATTING_CHOICES,
                help_text='Select the formatting rules that apply this image. By default, images'
                          ' will span 100% of the width of the text column. Selecting 50% would'
                          ' render the image so that the width occupied 50% of the text column.'
                          ' Aspect ratios will be preserved. For a somewhat technical explanation'
                          ' of how images work in Wagtail, see https://docs.wagtail.io/en/v2.12.3/topics/images.html'
            ))],
            icon='image', )
         ),
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
            FieldPanel('lead_image'),
            FieldPanel('lead_image_text'),  # Remove post migration
            FieldPanel('lead_image_caption'),
            FieldPanel('lead_image_alt_text'),
            FieldPanel('lead_image_formatting_options'),
        ], heading='Lead'),
        FieldPanel('body')
    ]

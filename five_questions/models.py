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
# from article.models import IMAGE_FORMATTING_CHOICES

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

# Image formatting choices.
IMAGE_FORMATTING_CHOICES = [
    ('25_PERCENT_WIDTH', '25% width'),
    ('50_PERCENT_WIDTH', '50% width'),
    ('75_PERCENT_WIDTH', '75% width'),
    ('90_PERCENT_WIDTH', '90% width'),
    ('100_PERCENT_WIDTH', '100% width'),
]


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
    # lead_image_text = models.CharField(max_length=255, blank=True, null=True)
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
        ('paragraph', blocks.RichTextBlock()),
        ('quote', blocks.BlockQuoteBlock()),
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
                                                          related_name='translations',
                                                          help_text = 'If this article is not in English, and there exists an '
                                                                      'English translation of the article, select it here. '
                                                                      'This will enable automatic linking of the various '
                                                                      'translations.',
                                                          )
    language = models.CharField(
        help_text="Specify the language in which the article is written. Note: the language must start with a"
                  " capital letter.",
        max_length=255
    )

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
            InlinePanel("authors", label="Author", min_num=0, max_num=10)
            # FieldPanel('name'),
            # FieldPanel('email'),
            # FieldPanel('twitter'),
            # FieldPanel('website'),
        ], heading='Author(s)'),
        MultiFieldPanel([
            ImageChooserPanel('lead_image'),
            FieldPanel('lead_image_caption'),
            FieldPanel('lead_image_alt_text'),
            FieldPanel('lead_image_formatting_options'),
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

from django.db import models
from django.shortcuts import render
from django.urls import reverse

from wagtail.admin.panels import FieldPanel
from wagtail import blocks
from wagtail.models import Page
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.fields import RichTextField, StreamField
from wagtail.images.blocks import ImageChooserBlock
from wagtail.embeds.blocks import EmbedBlock
from wagtail.images.models import Image
from wagtail.search.models import Query
from wagtail.admin.panels import FieldPanel
from wagtail.snippets.models import register_snippet
from wagtail.search import index


class HomePage(RoutablePageMixin, Page):
    """ The home page. """
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('body', classname='full'),
    ]

    def get_context(self, request):
        """
        Modify the QuerySet to return the three most recent published Resources and Articles.
        """
        # Avoid circular imports.
        # from issue.models import IssuePage
        from article.models import ArticlePage
        from resources.models import ResourcePage
        from five_questions.models import FiveQuestionsPage
        from invitations.models import InvitationsPage

        # Add the last three Resources and Issues to the context.
        context = super().get_context(request)
        # issuepages = IssuePage.objects.live().order_by('-first_published_at')[:3]
        # issuepages = reversed(issuepages)
        # context['issuepages'] = issuepages
        articlepages = ArticlePage.objects.live().public().order_by('-first_published_at').filter(language='English')[:3]
        articlepages = reversed(articlepages)
        context['articlepages'] = articlepages
        resourcepages = ResourcePage.objects.live().public().order_by('-first_published_at')[:3]
        resourcepages = reversed(resourcepages)
        context['resourcepages'] = resourcepages
        five_questionspages = FiveQuestionsPage.objects.live().public().order_by('-first_published_at').filter(models.Q(is_suppressed=False))[:1]
        five_questionspages = reversed(five_questionspages)
        context['five_questionspages'] = five_questionspages
        invitationspages = InvitationsPage.objects.live().public().filter(depth=4).order_by('-first_published_at')[:1]
        invitationspages = reversed(invitationspages)
        context['invitationspages'] = invitationspages

        return context

    @route(r'^s/$', name='s')
    def post_search(self, request, *args, **kwargs):
        """ Search for the site. """
        search_query = request.GET.get('q', '')  # Blank search box
        if search_query:
            search_results = Page.objects.live().public().search(search_query)
            # Log the query so Wagtail can suggest promoted results
            Query.get(search_query).add_hit()
        else:
            search_results = Page.objects.none()

        # Render template
        return render(request, 'home/search_results.html', {
            'search_query': search_query,
            'search_results': search_results,
        })


class AboutPage(Page):
    """
    The About page. Currently used as a generic blank page for About,
    Privacy Policy, Conntact us, etc.
    """
    body = RichTextField(blank=True)
    content_panels = Page.content_panels + [
        FieldPanel('body', classname='full'),
    ]


# Image formatting choices.
IMAGE_FORMATTING_CHOICES = [
    ('25_PERCENT_WIDTH', '25% width'),
    ('50_PERCENT_WIDTH', '50% width'),
    ('75_PERCENT_WIDTH', '75% width'),
    ('90_PERCENT_WIDTH', '90% width'),
    ('100_PERCENT_WIDTH', '100% width'),
]


class GenericPageIndex(Page):
    """
    GenericPageIndex just holds GenericPage(s) within the admin panel. There is
    no associted template and it's not for displaying anything on the front
    end.
    """
    subpage_types = ['home.GenericPage',]
    parent_page_type = ['wagtailcore.page',]

class GenericPage(Page):
    """ A generic page for one-off pages. """
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
    ], use_json_field=True)

    subpage_types = []

    parent_page_type = [
        'home.GenericIndexPage',
    ]

    search_fields = Page.search_fields + [
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('body'),
    ]


@register_snippet
class Copyright(models.Model):
    """ Snippet for editing the copyright text. """
    text = models.CharField(max_length=255)

    panels = [
        FieldPanel('text')
    ]

    class Meta:  # noqa
        verbose_name = 'Copyright text'
        verbose_name_plural = 'Copyright text'

    def __str__(self):
        return self.text


@register_snippet
class PrivacyPolicy(models.Model):
    """ Snippet for editing the privacy policy text and slug. """
    text = models.CharField(max_length=255)
    slug = models.CharField(max_length=255)

    panels = [
        FieldPanel('text'),
        FieldPanel('slug'),
    ]

    class Meta:  # noqa
        verbose_name = 'Privacy policy: text and slug'
        verbose_name_plural = 'Privacy policy: text and slug'

    def __str__(self):
        return self.text


@register_snippet
class TermsOfUse(models.Model):
    """ Snippet for editing the terms of use text and slug. """
    text = models.CharField(max_length=255)
    slug = models.CharField(max_length=255)

    panels = [
        FieldPanel('text'),
        FieldPanel('slug'),
    ]

    class Meta:  # noqa
        verbose_name = 'Terms of use: text and slug'
        verbose_name_plural = 'Terms of use: text and slug'

    def __str__(self):
        return self.text


@register_snippet
class Subscribe(models.Model):
    """ Snippet for controlling the 'click here to subscribe to understory' text. """
    text = models.CharField(max_length=255)
    url = models.URLField(max_length=255)

    panels = [
        FieldPanel('text'),
        FieldPanel('url'),
    ]

    class Meta:  # noqa
        verbose_name = 'Click here to subscribe: text and slug'
        verbose_name_plural = 'Click here to subscribe: text and slug'

    def __str__(self):
        return self.text

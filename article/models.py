""" understory/article/models.py """
from django.db import models
from django.shortcuts import render

from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase
from wagtail.admin.edit_handlers import (
    FieldPanel,
    InlinePanel,
    MultiFieldPanel,
    StreamFieldPanel,
)
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.core import blocks
from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField, StreamField
from wagtail.images.blocks import ImageChooserBlock
from wagtail.embeds.blocks import EmbedBlock
from wagtail.images.models import Image
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
from wagtail.snippets.models import register_snippet

from home.models import HomePage
from issue.models import IssuePage
from five_questions.models import FiveQuestionsPage


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


class TagIndexPage(Page):
    """
    Model for the article tags.
    """
    def get_context(self, request):
        """ Specify a QuerySet to return. """
        from blog.models import BlogPage  # Avoid circular import
        # Filter by tag
        tag = request.GET.get('tag')
        articlepages = ArticlePage.objects.live().public().filter(tags__name=tag)
        blogpages = BlogPage.objects.live().public().filter(tags__name=tag)
        imagepages = Image.objects.filter(tags__name=tag)
        five_questionspages = FiveQuestionsPage.objects.filter(tags__name=tag)

        # Update the template context
        context = super().get_context(request)
        context['articlepages'] = articlepages
        context['blogpages'] = blogpages
        context['imagepages'] = imagepages
        context['five_questionspages'] = five_questionspages

        return context


class TagPage(TaggedItemBase):
    """
    Support for tagging individual articles.
    """
    content_object = ParentalKey(
        'ArticlePage',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )


class ArticleIndexPage(Page):
    """
    The main article index page model.
    Location: /articles
    """
    intro = RichTextField(blank=True)

    def get_context(self, request):
        """
        Modify QuerySet to return posts in reverse chronological order and only return articles
        that are published.
        """
        context = super().get_context(request)
        articlepages = self.get_children().live().public().order_by('-first_published_at')
        context['articlepages'] = articlepages
        return context

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname='full')
    ]

    subpage_types = [
        'article.ArticlePage',
    ]

    parent_page_type = [
        'wagtailcore.page',
    ]


# Image formatting choices.
IMAGE_FORMATTING_CHOICES = [
    ('25_PERCENT_WIDTH', '25% width'),
    ('50_PERCENT_WIDTH', '50% width'),
    ('75_PERCENT_WIDTH', '75% width'),
    ('90_PERCENT_WIDTH', '90% width'),
    ('100_PERCENT_WIDTH', '100% width'),
]


class ArticlePage(Page):
    """
    Article page model. Formed from form input from ArticleSubmitPage and ArticleSubmitForm.
    Location: /articles/<article-slug>
    """

    # name = models.CharField(max_length=255)  # Author name
    # email = models.EmailField(max_length=255)  # Author email
    # twitter = models.CharField(max_length=255, blank=True, null=True)
    # website = models.URLField(max_length=255, blank=True, null=True)
    lead_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
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
    # Maybe the byline should be done similar to the blog categories with another model?
    # byline = models.CharField(max_length=255, blank=False, null=True, choices=BYLINE_CHOICES, default='name')
    # story_title = models.CharField(max_length=255)
    # body = RichTextField(blank=True)
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
    ])
    # Not displayed on the submission form.
    tags = ClusterTaggableManager(through=TagPage, blank=True)
    status = models.CharField(max_length=255, default='not_reviewed', choices=ARTICLE_STATUS)
    date = models.DateField('Post date', null=True, blank=True)
    intro = RichTextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # issue = ParentalKey(IssuePage, on_delete=models.SET_NULL, related_name='articles',
    #                     blank=True, null=True)
    issue = models.ForeignKey(
        IssuePage,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='articles',
        help_text="This field is historical and not currently used. It may be removed in the future.")
    # https://stackoverflow.com/questions/40554215/wagtail-filter-results-of-an-inlinepanel-foreignkey
    associated_English_article = models.ForeignKey('self', on_delete=models.SET_NULL,
                                                   null=True, blank=True,
                                                   related_name='translations',
                                                   help_text='If this article is not in English, and there exists an '
                                                             'English translation of the article, select it here. '
                                                             'This will enable automatic linking of the various '
                                                             'translations.'
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
            FieldPanel('issue'),
            FieldPanel('status'),
            FieldPanel('language'),
            FieldPanel('associated_English_article'),
        ], heading='Editorial information'),
    ]


class ArticleSubmitPage(Page):
    """
    Wagtail page view for article submission.
    Location: /submit
    """
    intro = RichTextField(blank=True)
    thank_you_page_title = models.CharField(
        max_length=255, help_text="Thank you for your submission.")
    thank_you = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname='full'),
        FieldPanel('thank_you_page_title'),
        FieldPanel('thank_you', classname='full'),
    ]

    def serve(self, request):
        """ Serve the submit form view. """
        from .forms import ArticleSubmitForm  # Avoid circular import.
        if request.method == 'POST':
            form = ArticleSubmitForm(request.POST)
            if form.is_valid():
                # Clean data
                name = form.cleaned_data['name']
                email = form.cleaned_data['email']
                twitter = form.cleaned_data['twitter']
                website = form.cleaned_data['website']
                # links = form.cleaned_data['links']
                story_title = form.cleaned_data['story_title']
                body = form.cleaned_data['body']

                # Set up the parent/child relationship between HomePage and ArticlePage
                index = ArticleIndexPage.objects.all()[0]  # Need at least one page.
                article = ArticlePage(
                    name=name,
                    email=email,
                    twitter=twitter,
                    website=website,
                    # links=links,
                    title=story_title,
                    body=body,
                )
                article.live = False  # Ensure articles do not go live by default.
                index.add_child(instance=article)
                article.save_revision()  # Save a revision so CMS user can compare to it.
                # index.save()
                return render(request, 'article/thank_you.html', {
                    'page': self,
                    'article': article,
                })
        else:
            form = ArticleSubmitForm()

        return render(request, 'article/submit.html', {
            'page': self,
            'form': form,
        })


class AuthorOrderable(Orderable):
    """ Enables selection of one or more authors from the Author snippet. See below. """
    page = ParentalKey("article.ArticlePage", related_name="authors", blank=True, null=True)
    author = models.ForeignKey(
        "article.Author",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    panels = [
        SnippetChooserPanel("author")
    ]


class InvitationsAuthorOrderable(Orderable):
    """ Enables selection of one or more authors from the Author snippet. See imported Author class. """
    page = ParentalKey("invitations.InvitationsPage", related_name="authors", blank=True, null=True)
    author = models.ForeignKey(
        "article.Author",  # Yes, this is where the F/K comes from, hence its location in this model.
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    panels = [
        SnippetChooserPanel("author")
    ]


class FiveQuestionsAuthorOrderable(Orderable):
    """ Enables selection of one or more authors from the Author snippet. See imported Author class. """
    page = ParentalKey("five_questions.FiveQuestionsPage", related_name="authors", blank=True, null=True)
    author = models.ForeignKey(
        "article.Author",  # Yes, this is where the F/K comes from, hence its location in this model.
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    panels = [
        SnippetChooserPanel("author")
    ]


class Author(models.Model):
    """ Author for articles (stories) and possibly more.
    Source:
    - https://learnwagtail.com/tutorials/registering-snippets-using-django-models/
    - https://learnwagtail.com/tutorials/using-snippetchooserpanel-select-multiple-blog-authors-snippets-orderables/
    """
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, blank=True, null=True)
    biography = models.TextField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    image = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
    )

    search_fields = Page.search_fields + [
        # index.SearchField('title'),  # This is redundant and causes an error.
        index.SearchField('name'),
        # index.SearchField('email'),
    ]

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("name"),
                ImageChooserPanel("image"),
                FieldPanel("biography"),
            ],
            heading="Biographical information"
        ),
        MultiFieldPanel(
            [
                FieldPanel("email"),
                FieldPanel("website")
            ],
            heading="Contact and links"
        ),
    ]

    def __str__(self):
        """ String representation of this class. """
        return self.name

    class Meta:  #noqa
        verbose_name = "Author"
        verbose_name_plural = "Authors"


register_snippet(Author)

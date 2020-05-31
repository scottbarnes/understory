""" understory/article/models.py """
from django.db import models
from django.shortcuts import render

# from autoslug import AutoSlugField
# from django_extensions.db.fields import AutoSlugField
from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField
from wagtail.search import index

from home.models import HomePage
from issue.models import IssuePage

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


# class Article(models.Model):
#     """
#     Article submission.
#     name: the applicant's name
#     email: the applicant's email. This will be validated for the form of a valid email address.
#     twitter: the applicant's twitter handle. No validation.
#     website: a website to which the applicant would like to link. Validation as to form.
#     links: a multi-select of 'links' the applicant would like to display with the byline:
#         - email, twitter, and website url.
#     story_title: the applicant's proposed story article.
#     body: the entire body of the applicant's article.
#     status: only for editors. Indicator of where the article is in the overall process. Statuses are:
#         - Not reviewed, In progress, and Review complete.
#
#     TODO:
#     - Add tags (for editors only?)
#     """
#
#     name = models.CharField(max_length=255)
#     email = models.EmailField(max_length=255)
#     twitter = models.CharField(max_length=255, blank=True, null=True)
#     website = models.URLField(max_length=255, blank=True, null=True)
#     # byline = models.CharField(max_length=255, blank=False, null=True, choices=BYLINE_CHOICES, default='name')
#     story_title = models.CharField(max_length=255)
#     body = models.TextField(max_length=9999)
#     # Not displayed on the submission form.
#     status = models.CharField(max_length=255, default='not_reviewed', choices=ARTICLE_STATUS)
#
#     def __str__(self):
#         return self.name


class ArticleIndexPage(Page):
    """
    The main article index page model.
    """
    intro = RichTextField(blank=True)

    def get_context(self, request):
        """
        Modify QuerySet to return posts in reverse chronological order and only return articles
        that are published.
        """
        context = super().get_context(request)
        articlepages = self.get_children().live().order_by('-first_published_at')
        context['articlepages'] = articlepages
        return context

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname='full')
    ]


class ArticlePage(Page):
    """
    Article page model. Formed from form input from ArticleSubmitPage and ArticleSubmitForm.
    """
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    twitter = models.CharField(max_length=255, blank=True, null=True)
    website = models.URLField(max_length=255, blank=True, null=True)
    # Maybe the byline should be done similar to the blog categories with another model?
    # byline = models.CharField(max_length=255, blank=False, null=True, choices=BYLINE_CHOICES, default='name')
    # story_title = models.CharField(max_length=255)
    body = RichTextField(blank=True)
    # Not displayed on the submission form.
    # slug = AutoSlugField(populate_from='body', editable=True)
    status = models.CharField(max_length=255, default='not_reviewed', choices=ARTICLE_STATUS)
    submitted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    issue = ParentalKey(IssuePage, on_delete=models.SET_NULL, related_name='articles',
                        blank=True, null=True)

    def __str__(self):
        return self.name

    # def save(self):
    #     self.slug = AutoSlugField(populate_from=self.title, editable=True)

    search_fields = Page.search_fields + [
        index.SearchField('title'),
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('name'),
            FieldPanel('email'),
            FieldPanel('twitter'),
            FieldPanel('website'),
        ], heading='Contact information'),
        FieldPanel('body'),
        FieldPanel('issue'),
        FieldPanel('status'),
    ]


class ArticleSubmitPage(Page):
    """ Wagtail page view for article submission. """
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
                index.save()
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

# class ArticleSubmitPage(Page):
#     """ Wagtail page view for article submission. """
#     intro = RichTextField(blank=True)
#     thank_you_page_title = models.CharField(
#         max_length=255, help_text="Thank you for your submission.")
#     thank_you = RichTextField(blank=True)
#
#     content_panels = Page.content_panels + [
#         FieldPanel('intro', classname='full'),
#         FieldPanel('thank_you_page_title'),
#         FieldPanel('thank_you', classname='full'),
#     ]
#
#     def serve(self, request):
#         """ Serve the submit form view. """
#         from .forms import ArticleSubmitForm  # Avoid circular import.
#         if request.method == 'POST':
#             form = ArticleSubmitForm(request.POST)
#             if form.is_valid():
#                 article = form.save()
#                 return render(request, 'article/thank_you.html', {
#                     'article': article,
#                     'page': self,
#                 })
#         else:
#             form = ArticleSubmitForm()
#
#         return render(request, 'article/submit.html', {
#             'page': self,
#             'form': form,
#         })
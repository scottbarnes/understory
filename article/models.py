""" understory/article/models.py """
from django.db import models
from django.shortcuts import render

from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core.models import Page
from wagtail.core.fields import RichTextField


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


class Article(models.Model):
    """
    Article submission.
    name: the applicant's name
    email: the applicant's email. This will be validated for the form of a valid email address.
    twitter: the applicant's twitter handle. No validation.
    website: a website to which the applicant would like to link. Validation as to form.
    links: a multi-select of 'links' the applicant would like to display with the byline:
        - email, twitter, and website url.
    story_title: the applicant's proposed story article.
    body: the entire body of the applicant's article.
    status: only for editors. Indicator of where the article is in the overall process. Statuses are:
        - Not reviewed, In progress, and Review complete.

    TODO:
    - Add tags (for editors only?)
    """

    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    twitter = models.CharField(max_length=255, blank=True, null=True)
    website = models.URLField(max_length=255, blank=True, null=True)
    byline = models.CharField(max_length=255, blank=False, null=True, choices=BYLINE_CHOICES, default='name')
    # links = models.CharField(max_length=255, blank=True, null=True)
    story_title = models.CharField(max_length=255)
    body = models.TextField(max_length=9999)
    # Not displayed on the submission form.
    status = models.CharField(max_length=255, default='not_reviewed', choices=ARTICLE_STATUS)


class ArticleSubmitPage(Page):
    """ Wagtail page view for article submission. """
    intro = RichTextField(blank=True)
    thank_you_page_title = models.CharField(
        max_length=255, help_text="Thank you for your submission.")

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname='full'),
        FieldPanel('thank_you_page_title'),
    ]

    def serve(self, request):
        """ Serve the submit form view. """
        from .forms import ArticleSubmitForm  # Avoid circular import.
        if request.method == 'POST':
            form = ArticleSubmitForm(request.POST)
            if form.is_valid():
                article = form.save()
                return render(request, 'article/thank_you.html', {
                    'article': article,
                    'page': self,
                })
        else:
            form = ArticleSubmitForm()

        return render(request, 'article/submit.html', {
            'page': self,
            'form': form,
        })

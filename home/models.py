from django.db import models
from django.shortcuts import render
from django.urls import reverse

from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core.models import Page
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.core.fields import RichTextField
from wagtail.search.models import Query
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.snippets.models import register_snippet


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
        five_questionspages = FiveQuestionsPage.objects.live().public().order_by('-first_published_at')[:1]
        five_questionspages = reversed(five_questionspages)
        context['five_questionspages'] = five_questionspages
        invitationspages = InvitationsPage.objects.live().public().order_by('-first_published_at')[:1]
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
    """ The About page. Currently used as a generic blank page. Should come up with another strategy with a
     Streamfield or something. """
    body = RichTextField(blank=True)
    content_panels = Page.content_panels + [
        FieldPanel('body', classname='full'),
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

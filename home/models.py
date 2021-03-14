from django.db import models
from django.shortcuts import render

from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core.models import Page
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.core.fields import RichTextField
from wagtail.search.models import Query


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

        # Add the last three Resources and Issues to the context.
        context = super().get_context(request)
        # issuepages = IssuePage.objects.live().order_by('-first_published_at')[:3]
        # issuepages = reversed(issuepages)
        # context['issuepages'] = issuepages
        articlepages = ArticlePage.objects.live().order_by('-first_published_at')[:3]
        articlepages = reversed(articlepages)
        context['articlepages'] = articlepages
        resourcepages = ResourcePage.objects.live().order_by('-first_published_at')[:3]
        resourcepages = reversed(resourcepages)
        context['resourcepages'] = resourcepages

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
    """ The About page. """
    body = RichTextField(blank=True)
    content_panels = Page.content_panels + [
        FieldPanel('body', classname='full'),
    ]






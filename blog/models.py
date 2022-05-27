""" understory/blog/models.py """
from django import forms
from django.db import models

from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.contrib.taggit import ClusterTaggableManager
from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.images.edit_handlers import FieldPanel
from wagtail.search import index
from wagtail.snippets.models import register_snippet

from taggit.models import TaggedItemBase


class BlogIndexPage(Page):
    """
    The main blog index page model.
    """
    intro = RichTextField(blank=True)

    def get_context(self, request):
        """
        Modify QuerySet to return posts in reverse chronological order and anly return posts
        that are published.
        """
        context = super().get_context(request)
        blogpages = self.get_children().live().order_by('-first_published_at')
        context['blogpages'] = blogpages
        return context

    subpage_types = [
        'blog.BlogPage',
    ]

    parent_page_type = [
        'wagtailcore.page',
    ]

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname='full')
    ]


class BlogTagIndexPage(Page):
    """
    Model for the tags view.
    """
    def get_context(self, request):
        """ Specify a QuerySet to return. """
        # Filter by tag
        tag = request.GET.get('tag')
        blogpages = BlogPage.objects.live().filter(tags__name=tag)

        # Update template context
        context = super().get_context(request)
        context['blogpages'] = blogpages
        return context


class BlogPageTag(TaggedItemBase):
    """
    Support for tagging posts.
    """
    content_object = ParentalKey(
        'BlogPage',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )


@register_snippet
class BlogCategory(models.Model):
    """
    Blog categories
    """
    name = models.CharField(max_length=255)
    icon = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='+'
    )

    panels = [
        FieldPanel('name'),
        FieldPanel('icon'),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'blog categories'


class BlogPage(Page):
    """
    Individual blog pages.
    """
    date = models.DateField('Post date')
    intro = models.CharField(max_length=250)
    body = RichTextField(blank=True)
    tags = ClusterTaggableManager(through=BlogPageTag, blank=True)
    categories = ParentalManyToManyField('blog.BlogCategory', blank=True)

    def main_image(self):
        """
        Return the first gallery image or None.
        """
        gallery_item = self.gallery_images.first()
        if gallery_item:
            return gallery_item.image
        else:
            return None

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('date'),
            FieldPanel('tags'),
            FieldPanel('categories', widget=forms.CheckboxSelectMultiple),
        ], heading='Blog information'),
        FieldPanel('intro'),
        FieldPanel('body'),
        InlinePanel('gallery_images', label='Gallery images'),
    ]


class BlogPageGalleryImage(Orderable):
    """
    Create an image gallery object to better control image layout and styling
    """
    page = ParentalKey(BlogPage, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
    )
    caption = models.CharField(blank=True, max_length=250)

    panels = [
        FieldPanel('image'),
        FieldPanel('caption'),
    ]

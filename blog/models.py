from django.db import models

from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase

from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index


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

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname='full')
    ]


class BlogPageTag(TaggedItemBase):
    """
    Support for tagging posts.
    """
    content_object = ParentalKey(
        'BlogPage',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )


class BlogPage(Page):
    """
    Individual blog pages.
    """
    date = models.DateField('Post date')
    intro = models.CharField(max_length=250)
    body = RichTextField(blank=True)
    tags = ClusterTaggableManager(through=BlogPageTag, blank=True)

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
        ], heading='Blog information'),
        FieldPanel('date'),
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
        ImageChooserPanel('image'),
        FieldPanel('caption'),
    ]

""" understory/blog/tests/models.py """

from wagtail.test.utils import WagtailPageTests
from blog.models import (
    BlogIndexPage, BlogPage,
)


class BlogTests(WagtailPageTests):

    def test_can_create_under_blog_page(self):
        self.assertCanCreateAt(BlogIndexPage, BlogPage)




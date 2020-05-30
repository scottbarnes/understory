""" understory/article/tests/test_forms.py """
from django.test import Client, TestCase
from django.shortcuts import reverse

from wagtail.core.models import Page

from ..forms import ArticleSubmitForm
from ..models import Article, ArticleSubmitPage


class ArticleFormTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_form_renders_with_content(self):
        """ Note: does not test crispy forms. """
        form = ArticleSubmitForm()
        self.assertIn('input type="text" name="name"', form.as_p())

    def test_form_renders_bootstrap_with_a_get(self):
        """
        For this to work I need to create the page in the test environment?
        Source: https://stackoverflow.com/questions/42649732/testing-wagtail-page-views-using-client-get
        """
        parent = Page.objects.get(url_path='/home/')
        page = ArticleSubmitPage(
            title='Article submission page',
            slug='submit',
            intro="Please enter your submission. We'll correspond with you via email.",
            thank_you_page_title='Thank you for your submission',
        )
        parent.add_child(instance=page)

        response = self.client.get('/submit/')
        self.assertIn(b'class="textinput textInput form-control"', response.content)


    def test_can_submit_article_form(self):
        pass

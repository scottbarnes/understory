""" understory/article/tests/test_forms.py """
from django.test import Client, TestCase
from django.shortcuts import reverse

from wagtail.core.models import Page

from ..forms import ArticleSubmitForm
from ..models import ArticlePage, ArticleSubmitPage, ArticleIndexPage


class ArticleFormTest(TestCase):

    def setUp(self):
        self.client = Client()
        # Create a page since they exist in the database and therefore don't exist in the test DB
        # Source: https://stackoverflow.com/questions/42649732/testing-wagtail-page-views-using-client-get
        parent = Page.objects.get(url_path='/home/')
        # parent = ArticleIndexPage.objects.get(url_path='/articles/')
        page = ArticleSubmitPage(
            title='Article submission page',
            slug='submit',
            intro="Please enter your submission. We'll correspond with you via email.",
            thank_you_page_title='Thank you for your submission',
        )
        parent.add_child(instance=page)

    def test_form_renders_with_content(self):
        """ Note: does not test crispy forms. """
        form = ArticleSubmitForm()
        self.assertIn('input type="text" name="name"', form.as_p())

    def test_form_renders_bootstrap_with_a_get(self):
        """ Note: does test crispy forms. """
        response = self.client.get('/submit/')
        self.assertIn(b'class="textinput textInput form-control"', response.content)

    def test_can_submit_article_form(self):
        response = self.client.post('/submit/', {
            'name': 'Tester McTest',
            'email': 'test@example.com',
            'twitter': '',
            'story_title': 'Test story title',
            'body': 'This is the test story body',
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ArticlePage.objects.count(), 1)
        self.assertEqual(ArticlePage.objects.last().name, 'Tester McTest')

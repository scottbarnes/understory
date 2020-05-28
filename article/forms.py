""" understory.article.forms.py """
from django import forms

from .models import Article


class ArticleSubmitForm(forms.Form):
    """
    Form to submit articles.
    """

    LINK_CHOICES = (
        ('email', 'Email '),
        ('twitter', 'Twitter'),
        ('website', 'Website'),
    )

    name = forms.CharField(max_length=255, label='Your name')
    email = forms.EmailField(max_length=255, label='Email address')
    twitter = forms.CharField(max_length=255, label='Twitter handle (optional)', required=False)
    website = forms.URLField(max_length=255, label='Website address (optional)', required=False)
    links = forms.MultipleChoiceField(choices=LINK_CHOICES, widget=forms.CheckboxSelectMultiple(),
                                      label='Select additional byline information (by default we\'ll only display your name):',
                                      required=False)
    story_title = forms.CharField(max_length=255, label='Article title')
    body = forms.CharField(label='Article body (just paste it all here)', widget=forms.Textarea)

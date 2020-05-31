""" understory.article.forms.py """
from django import forms

from .models import ArticlePage


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
    # links = forms.MultipleChoiceField(choices=LINK_CHOICES, widget=forms.CheckboxSelectMultiple(),
    #                                   label='Select additional byline information (by default we\'ll only display '
    #                                         'your name):',
    #                                   required=False)
    story_title = forms.CharField(max_length=255, label='Article title')
    body = forms.CharField(label='Article body (just paste it all here)', widget=forms.Textarea)


# class ArticleSubmitForm(forms.ModelForm):
#     """
#     Form to submit articles
#     """
#
#     class Meta:
#         model = Article
#
#         fields = (
#             'name',
#             'email',
#             'twitter',
#             'website',
#             # 'byline',
#             'story_title',
#             'body',
#         )
#         widgets = {
#             # 'links': forms.MultipleChoiceField(choices=LINK_CHOICES, widget=forms.CheckboxSelectMultiple()),
#             # 'byline': forms.CheckboxSelectMultiple(),
#             'body': forms.Textarea(),
#         }
#         labels = {
#             'twitter': 'Twitter handle (optional)',
#             'website': 'Website address (optional)',
#             # 'byline': 'Things to include in your byline (by default we only include names)',
#             'story_title': 'Article title',
#             'body': 'Just paste your entire article here',
#         }
#         help_texts = {
#             'website': 'Note: be sure to include the "http://" prefix',
#         }



""" understory.article.forms.py """
from django import forms

from .models import Article


class ArticleSubmitForm(forms.ModelForm):
    """
    Form to submit articles
    """

    class Meta:
        model = Article

        fields = (
            'name',
            'email',
            'twitter',
            'website',
            'byline',
            'story_title',
            'body',
        )
        widgets = {
            # 'links': forms.MultipleChoiceField(choices=LINK_CHOICES, widget=forms.CheckboxSelectMultiple()),
            'byline': forms.CheckboxSelectMultiple(),
            'body': forms.Textarea(),
        }
        labels = {
            'twitter': 'Twitter handle (optional)',
            'website': 'Website address (optional)',
            # 'byline': 'Things to include in your byline (by default we only include names)',
            'story_title': 'Article title',
            'body': 'Just paste your entire article here',
        }
        help_texts = {
            'website': 'Note: be sure to include the "http://" prefix',
        }



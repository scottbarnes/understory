# Generated by Django 3.0.6 on 2020-05-28 17:48

from django.db import migrations
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0004_article_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='articlesubmitpage',
            name='intro',
            field=wagtail.core.fields.RichTextField(blank=True),
        ),
    ]
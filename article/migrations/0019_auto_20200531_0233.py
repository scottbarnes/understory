# Generated by Django 3.0.6 on 2020-05-31 02:33

from django.db import migrations
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0018_articleindexpage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articlepage',
            name='body',
            field=wagtail.core.fields.RichTextField(blank=True),
        ),
    ]
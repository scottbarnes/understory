# Generated by Django 3.1.7 on 2021-03-25 11:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0031_auto_20200911_2134'),
    ]

    operations = [
        migrations.RenameField(
            model_name='articlepage',
            old_name='associated_english_article',
            new_name='associated_English_article',
        ),
    ]

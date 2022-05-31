# Generated by Django 4.0.4 on 2022-05-30 19:56

import common.util.language_field
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0055_alter_articlepage_body'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articlepage',
            name='language',
            field=common.util.language_field.LanguageField(help_text='Specify the language in which the Story is written.', max_length=255),
        ),
    ]

# Generated by Django 4.0.4 on 2022-05-30 19:56

import common.util.language_field
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('five_questions', '0009_alter_fivequestionspage_body'),
    ]

    operations = [
        migrations.RenameField(
            model_name='fivequestionspage',
            old_name='associated_English_five_questions',
            new_name='associated_English_article',
        ),
        migrations.AlterField(
            model_name='fivequestionspage',
            name='language',
            field=common.util.language_field.LanguageField(help_text='Specify the language in which the Five Questions iswritten.', max_length=255),
        ),
    ]

# Generated by Django 4.0.4 on 2022-05-16 01:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0052_alter_articlepage_body'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articlepage',
            name='associated_English_article',
            field=models.ForeignKey(blank=True, help_text='If this Story is not in English, and there exists an English translation of the Story, select it here. This will enable automatic linking of the various translations.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='translations', to='article.articlepage'),
        ),
        migrations.AlterField(
            model_name='articlepage',
            name='language',
            field=models.CharField(help_text='Specify the language in which the Story is written. Note: the language must start with a capital letter.', max_length=255),
        ),
    ]

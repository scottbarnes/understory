# Generated by Django 3.0.6 on 2020-05-28 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='links',
            field=models.CharField(blank=True, choices=[('email', 'Email'), ('twitter', 'Twitter'), ('website', 'Website')], max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='article',
            name='website',
            field=models.URLField(blank=True, max_length=255, null=True),
        ),
    ]
# Generated by Django 3.0.6 on 2020-05-28 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0002_auto_20200528_1629'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='links',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]

# Generated by Django 3.0.6 on 2020-06-12 20:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0024_auto_20200602_2139'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='articlepage',
            name='issue',
        ),
    ]
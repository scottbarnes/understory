# Generated by Django 4.0.4 on 2022-05-16 01:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0052_alter_articlepage_body'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='articlepage',
            name='issue',
        ),
    ]

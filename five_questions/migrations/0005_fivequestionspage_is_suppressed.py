# Generated by Django 3.1.12 on 2021-11-04 19:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('five_questions', '0004_fivequestionspage_is_flipbook'),
    ]

    operations = [
        migrations.AddField(
            model_name='fivequestionspage',
            name='is_suppressed',
            field=models.BooleanField(default=False),
        ),
    ]
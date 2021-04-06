# Generated by Django 3.1.7 on 2021-04-05 23:04

from django.db import migrations
import django.db.models.deletion
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('five_questions', '0001_initial'),
        ('article', '0036_fivequestionsauthororderable'),
    ]

    operations = [
        migrations.AddField(
            model_name='fivequestionsauthororderable',
            name='page',
            field=modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='authors', to='five_questions.fivequestionspage'),
        ),
    ]

# Generated by Django 3.1.7 on 2021-04-06 19:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0041_auto_20210406_1902'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fivequestionsauthororderable',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='article.author'),
        ),
    ]
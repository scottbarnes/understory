# Generated by Django 3.0.6 on 2020-06-12 20:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('issue', '0002_issuepage_image'),
        ('article', '0025_remove_articlepage_issue'),
    ]

    operations = [
        migrations.AddField(
            model_name='articlepage',
            name='issue',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='articles', to='issue.IssuePage'),
        ),
    ]
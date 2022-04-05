# Generated by Django 4.0.2 on 2022-04-05 03:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0004_alter_taggeditem_content_type_alter_taggeditem_tag'),
        ('blog', '0009_auto_20200609_1755'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpagetag',
            name='tag',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_items', to='taggit.tag'),
        ),
    ]

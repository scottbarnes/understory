# Generated by Django 3.0.6 on 2020-06-02 21:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import modelcluster.contrib.taggit
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('wagtailredirects', '0006_redirect_increase_max_length'),
        ('wagtailcore', '0045_assign_unlock_grouppagepermission'),
        ('contenttypes', '0002_remove_content_type_name'),
        ('wagtailforms', '0004_add_verbose_name_plural'),
        ('taggit', '0003_taggeditem_add_unique_index'),
        ('article', '0023_auto_20200531_2322'),
    ]

    operations = [
        migrations.CreateModel(
            name='TagPage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content_object', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='tagged_items', to='article.ArticlePage')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='article_tagpage_items', to='taggit.Tag')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RenameModel(
            old_name='ArticleTagIndexPage',
            new_name='TagIndexPage',
        ),
        migrations.DeleteModel(
            name='ArticleTagPage',
        ),
        migrations.AlterField(
            model_name='articlepage',
            name='tags',
            field=modelcluster.contrib.taggit.ClusterTaggableManager(blank=True, help_text='A comma-separated list of tags.', through='article.TagPage', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]
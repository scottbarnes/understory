# Generated by Django 3.1.7 on 2021-03-28 18:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_copyright'),
    ]

    operations = [
        migrations.CreateModel(
            name='PrivacyPolicy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=255)),
                ('slug', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'Privacy policy text and slug',
                'verbose_name_plural': 'Privacy policy text and slug',
            },
        ),
        migrations.CreateModel(
            name='TermsOfUse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=255)),
                ('slug', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'Terms of use text and slug',
                'verbose_name_plural': 'Terms of use text and slug',
            },
        ),
        migrations.AlterModelOptions(
            name='copyright',
            options={'verbose_name': 'Copyright text', 'verbose_name_plural': 'Copyright text'},
        ),
    ]

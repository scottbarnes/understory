# Generated by Django 3.1.7 on 2021-03-28 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_aboutpage'),
    ]

    operations = [
        migrations.CreateModel(
            name='Copyright',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=255)),
            ],
        ),
    ]

# Generated by Django 3.1.7 on 2021-04-05 23:46

from django.db import migrations
import django.db.models.deletion
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0038_invitationsauthororderable'),
        ('invitations', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='invitationsauthororderable',
            name='page',
            field=modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='authors', to='invitations.invitationspage'),
        ),
    ]
# Generated by Django 4.0.4 on 2022-05-16 01:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('five_questions', '0007_alter_fivequestionspage_body'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fivequestionspage',
            name='associated_English_five_questions',
            field=models.ForeignKey(blank=True, help_text='If this Five Questions is not in English, and there exists an English translation of the Five Questions , select it here. This will enable automatic linking of the various translations.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='translations', to='five_questions.fivequestionspage'),
        ),
        migrations.AlterField(
            model_name='fivequestionspage',
            name='language',
            field=models.CharField(help_text='Specify the language in which the Five Questions is written. Note: the language must start with a capital letter.', max_length=255),
        ),
    ]

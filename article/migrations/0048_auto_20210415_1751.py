# Generated by Django 3.1.7 on 2021-04-15 17:51

from django.db import migrations, models
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0047_auto_20210415_1653'),
    ]

    operations = [
        migrations.AddField(
            model_name='articlepage',
            name='lead_image_formatting_options',
            field=models.CharField(choices=[('25_PERCENT_WIDTH', '25% width'), ('50_PERCENT_WIDTH', '50% width'), ('75_PERCENT_WIDTH', '75% width'), ('100_PERCENT_WIDTH', '100% width')], default='100_PERCENT_WIDTH', max_length=255),
        ),
        migrations.AlterField(
            model_name='articlepage',
            name='body',
            field=wagtail.core.fields.StreamField([('heading', wagtail.core.blocks.CharBlock(form_classname='full title')), ('paragraph', wagtail.core.blocks.RichTextBlock()), ('quote', wagtail.core.blocks.BlockQuoteBlock()), ('image', wagtail.images.blocks.ImageChooserBlock()), ('image_with_alt_text', wagtail.core.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock()), ('caption_text', wagtail.core.blocks.RichTextBlock(required=False)), ('alt_text', wagtail.core.blocks.TextBlock(help_text='Specify the alt text to improve site accessibility. This should be  descriptive of the image and not merely a recitation of the caption text. Nor should it be duplicative of information in the caption. But it should be pithy. Perhaps no more than 125 characters. See best practices at https://axesslab.com/alt-texts/.')), ('formatting_options', wagtail.core.blocks.ChoiceBlock(choices=[('25_PERCENT_WIDTH', '25% width'), ('50_PERCENT_WIDTH', '50% width'), ('75_PERCENT_WIDTH', '75% width'), ('100_PERCENT_WIDTH', '100% width')], help_text='Select the formatting rules that apply this image. By default, images will span 100% of the width of the text column. Selecting 50% would render the image so that the width occupied 50% of the text column. Aspect ratios will be preserved. For a somewhat technical explanation of how images work in Wagtail, see https://docs.wagtail.io/en/v2.12.3/topics/images.html', required=False))], icon='image')), ('image_text', wagtail.core.blocks.RichTextBlock()), ('embeded_item', wagtail.core.blocks.RawHTMLBlock())]),
        ),
    ]

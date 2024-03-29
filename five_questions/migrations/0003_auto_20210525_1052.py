# Generated by Django 3.1.7 on 2021-05-25 10:52

from django.db import migrations
import wagtail.blocks
import wagtail.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('five_questions', '0002_auto_20210424_1118'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fivequestionspage',
            name='lead_image_text',
        ),
        migrations.AlterField(
            model_name='fivequestionspage',
            name='body',
            field=wagtail.fields.StreamField([('heading', wagtail.blocks.CharBlock(form_classname='full title')), ('paragraph', wagtail.blocks.RichTextBlock()), ('quote', wagtail.blocks.BlockQuoteBlock()), ('image_with_alt_text', wagtail.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock()), ('caption_text', wagtail.blocks.RichTextBlock(required=False)), ('alt_text', wagtail.blocks.TextBlock(help_text='Specify the alt text to improve site accessibility. This should be  descriptive of the image and not merely a recitation of the caption text. Nor should it be duplicative of information in the caption. But it should be pithy. Perhaps no more than 125 characters. See best practices at https://axesslab.com/alt-texts/.')), ('formatting_options', wagtail.blocks.ChoiceBlock(choices=[('25_PERCENT_WIDTH', '25% width'), ('50_PERCENT_WIDTH', '50% width'), ('75_PERCENT_WIDTH', '75% width'), ('90_PERCENT_WIDTH', '90% width'), ('100_PERCENT_WIDTH', '100% width')], help_text='Select the formatting rules that apply this image. By default, images will span 100% of the width of the text column. Selecting 50% would render the image so that the width occupied 50% of the text column. Aspect ratios will be preserved. For a somewhat technical explanation of how images work in Wagtail, see https://docs.wagtail.io/en/v2.12.3/topics/images.html', required=False))], icon='image')), ('embeded_item', wagtail.blocks.RawHTMLBlock())]),
        ),
    ]

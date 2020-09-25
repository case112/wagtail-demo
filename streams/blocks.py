""" Streamfields live in here """

from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock

class TitleAndTextBlock(blocks.StructBlock):
    """ Title and text and nothing else """

    title = blocks.CharBlock(requred=True, help_text='Add your title')
    text = blocks.TextBlock(required=True, help_text='Additional text')

    class Meta:
        template = 'streams/title_and_text_block.html'
        icon = 'edit'
        label = 'Title & text'


class CardBlock(blocks.StructBlock):
    """ Cards with image and text and button """

    title = blocks.CharBlock(requred=True, help_text='Add your title')

    cards = blocks.ListBlock(
        blocks.StructBlock(
            [
                ('image', ImageChooserBlock(required=True)),
                ('title', blocks.CharBlock(required=True, max_length=40)),
                ('text', blocks.TextBlock(required=True, max_length=200)),
                ('button_page', blocks.PageChooserBlock(required=False)),
                ('button_url', blocks.URLBlock(required=False, help_text='If the button page above is selected, that will be used first.')),
            ]
        )
    )

    class Meta:
        template = 'streams/card_block.html'
        icon = 'placeholder'
        label = 'Staff Cards'


class RichTextBlock(blocks.RichTextBlock):
    """ Richtext with all the features """

    class Meta:
        template = 'streams/richtext_block.html'
        icon = 'edit'
        label = 'Full RichText'


class CTABlock(blocks.StructBlock):

    title = blocks.CharBlock(required=True, max_length=50)
    text = blocks.RichTextBlock(required=True, features=['bold', 'italic'])
    button_page = blocks.PageChooserBlock(required=False)
    button_url = blocks.URLBlock(required=False)
    button_text = blocks.CharBlock(requred=True, default='Learn More', max_length=40)

    class Meta:
        template = 'streams/cta_block.html'
        icon = 'placeholder'
        label = 'Call to Action'
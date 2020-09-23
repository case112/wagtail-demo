""" Streamfields live in here """

from wagtail.core import blocks

class TitleAndTextBlock(blocks.StructBlock):
    """ Title and text and nothing else """

    title = blocks.CharBlock(requred=True, help_text='Add your title')
    text = blocks.TextBlock(required=True, help_text='Additional text')

    class Meta:
        template = 'streams/title_and_text_block.html'
        icon = 'edit'
        label = 'Title & text'
        

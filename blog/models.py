from django.db import models

from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.core.models import Page 
from wagtail.core.fields import StreamField
from wagtail.images.edit_handlers import ImageChooserPanel

from streams import blocks

class BlogListingPage(Page):
    """ Listing page lists all the Blog Detail Pages """

    custom_title = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        help_text='Add your title',
    )

    content_panels = Page.content_panels + [
        FieldPanel('custom_title'), 
    ]

    def get_context(self, request, *args, **kwargs):
        """ Adding custom stuff to our context """
        context = super().get_context(request, *args, **kwargs)
        #context['extra'] = 'Read all about it' 
        return context


class BlogDetailPage():
    """ Blog Detail page """

    custom_title = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        help_text='Add your title',
    )

    blog_image = models.ForeignKey(
        'wagtailimages.Image',
        blank=False,
        null=True,
        related_name='+',
        on_delete=models.SET_NULL,
    )

    content = StreamField(
        [
            ('title_and_text', blocks.TitleAndTextBlock()),
            ('full_richtext', blocks.RichTextBlock()),
            ('cards', blocks.CardBlock()),
            ('cta', blocks.CTABlock()),
        ],
        null=True,
        blank=True
    )

    content_panels = Page.content_panels + [
        FieldPanel('custom_title'),
        ImageChooserPanel('blog_image'),
        StreamFieldPanel('content'),
    ]

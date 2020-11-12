from django.db import models
from django.shortcuts import render

from modelcluster.fields import ParentalKey

from wagtail.api import APIField
from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField, StreamField
from wagtail.admin.edit_handlers import FieldPanel, PageChooserPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel, StreamFieldPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, route

from streams import blocks 

class HomePageCarouselImages(Orderable):
    """ Between 1 and 5 images for the home page carousel """

    page = ParentalKey('home.HomePage', related_name='carousel_images')
    #label = models.CharField(max_length=70, null=True, blank=True)
    #sublabel = RichTextField(features=['bold', 'italic'], null=True, blank=True)
    carousel_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    panels = [
        #FieldPanel('label'),
        #FieldPanel('sublabel'),
        ImageChooserPanel('carousel_image')
    ]

    api_fields = [
        APIField('carousel_image'),
    ]


class HomePage(RoutablePageMixin, Page):
    templates = 'home/home_page.html'

    subpage_types = [
        'blog.BlogListingPage',
        'contact.ContactPage',
        'flex.FlexPage',    
    ]
    parent_page_type = [
        'wagtailcore.Page'
    ]
    #max_count = 1

    banner_title = models.CharField(max_length=100, blank=False, null=True)
    banner_subtitle = RichTextField(features=['bold', 'italic'])
    banner_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    banner_cta = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    content = StreamField(
        [
            ('cta', blocks.CTABlock()),
        ],
        null=True,
        blank=True
    )

    api_fields = [
        APIField('banner_title'),
        APIField('banner_subtitle'),
        APIField('banner_image'),
        APIField('banner_cta'),
        APIField('carousel_images'),
        APIField('content'),
    ]

    max_count = 1

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('banner_title'),
            FieldPanel('banner_subtitle'),
            ImageChooserPanel('banner_image'),
            PageChooserPanel('banner_cta'),
        ], heading='Banner Options'),
        MultiFieldPanel([
            #FieldPanel('label'),
            #FieldPanel('sublabel'),
            InlinePanel('carousel_images', max_num=5, min_num=1, label='Image'),
        ], heading='Caorusel Images'),
        StreamFieldPanel('content'),

    ]

    @route(r'^subscribe/$')
    def the_subscribe_page(self, request, *args, **kwargs):
        context = self.get_context(request, *args, **kwargs)
        return render(request, 'home/subscribe.html', context)

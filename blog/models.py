from django.db import models
from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key
from django.shortcuts import render
from django import forms
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from wagtail.api import APIField 
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from wagtail.admin.edit_handlers import (
    FieldPanel,
    StreamFieldPanel,
    MultiFieldPanel,
    InlinePanel,

)
from wagtail.core.models import Page, Orderable
from wagtail.core.fields import StreamField

from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.snippets.models import register_snippet

from streams import blocks 

from rest_framework.fields import Field

class ImageSerializedField(Field):
    def to_representation(self, value):
        return {
            'url': value.file.url,
            'title': value.title,
            'width': value.width,
            'height': value.height,
        }



class BlogAuthorOrderable(Orderable):
    """ This allows us to select one or more authors to a post """

    page = ParentalKey('blog.BlogDetailPage', related_name='blog_authors')
    author = models.ForeignKey(
        'blog.BlogAuthor',
        on_delete=models.CASCADE,
    )

    panels = [
        SnippetChooserPanel('author'),
    ]

    @property
    def author_name(self):
        return self.author.name
    
    @property
    def author_website(self):
        return self.author.website
    
    @property
    def author_image(self):
        return self.author.image

    api_fields = [
        APIField('author_name'),
        APIField('author_website'),
        APIField('author_image', serializer=ImageSerializedField()),
        ]



class BlogAuthor(models.Model):
    """ Blog author for snippets """

    name = models.CharField(max_length=100)
    website = models.URLField(blank=True, null=True)
    image = models.ForeignKey(
        'wagtailimages.Image',
        blank=False,
        null=True,
        related_name='+',
        on_delete=models.SET_NULL,
    )

    panels = [
        MultiFieldPanel(
            [
                FieldPanel('name'),
                ImageChooserPanel('image')
            ],
            heading='Name and Image'
        ),
        MultiFieldPanel(
            [
                FieldPanel('website'),
            ],
            heading='Links'
        ),
    ]

    def __str__(self):
        """ String repr of this class """
        return self.name

    class Meta:
        verbose_name = 'Blog Author'
        verbose_name_plural = 'Blog Authors'


register_snippet(BlogAuthor)


class BlogCategory(models.Model):
    """ Blog category for a snippet """

    name = models.CharField(max_length=255)
    slug = models.SlugField(
        verbose_name='slug',
        allow_unicode=True,
        max_length=255,
        help_text='A slug to indentify posts by this category',
    )

    panels = [
        FieldPanel('name'),
        FieldPanel('slug'),
    ]    

    class Meta:
        verbose_name ='Blog Category'
        verbose_name_plural ='Blog Categories'
        ordering = ['name']

    def __str__(self):
        """ String repr of this class """
        return self.name


register_snippet(BlogCategory)


class BlogListingPage(RoutablePageMixin, Page):
    """ Listing page lists all the Blog Detail Pages """

    template = 'blog/blog_listing_page.html'

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
        all_posts = BlogDetailPage.objects.live().public().order_by('-first_published_at')
        paginator = Paginator(all_posts, 2)
        page = request.GET.get('page')

        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)

        context['posts'] = posts
        
        context['categories'] = BlogCategory.objects.all()
        return context

    @route(r'^latest/?$', name='latest_posts')
    def latest_blog_posts(self, request, *args, **kwargs):
        context = self.get_context(request, *args, **kwargs)
        context['posts'] = context['posts'][:2]
        return render(request, 'blog/latest_posts.html', context)

    def get_sitemap_urls(self, request):
        # return [] # Uncomment to have no sitemap for this page
        sitemap = super().get_sitemap_urls(request)
        sitemap.append(
            {
                'location': self.full_url + self.reverse_subpage('latest_posts'),
                'lastmod': (self.last_published_at or self.latest_revision_created_at),
                'priority': 0.9, 
            }
        )
        return sitemap

class BlogDetailPage(Page):
    """ Parental blog Detail page """

    custom_title = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        help_text='Add your title',
    )

    banner_image = models.ForeignKey(
        'wagtailimages.Image',
        blank=False,
        null=True,
        related_name='+',
        on_delete=models.SET_NULL,
    )

    categories = ParentalManyToManyField('blog.BlogCategory', blank=True)

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
        ImageChooserPanel('banner_image'),
        StreamFieldPanel('content'),
        MultiFieldPanel(
            [
                InlinePanel('blog_authors', label='Author', min_num=1, max_num=4)
            ],
            heading='Authors'
        ),
        MultiFieldPanel(
            [
                FieldPanel('categories', widget=forms.CheckboxSelectMultiple)
            ],
            heading='Categories'
        ), 
    ]

    api_fields = [
        APIField('blog_authors'),
        APIField('content'),
    ]

    def save(self, *args, **kwargs):
        key = make_template_fragment_key('blog_post_preview', [self.id])
        cache.delete(key)
        return super().save(*args, **kwargs)


class ArticleBlogPage(BlogDetailPage):
    """ A subclassed blog post page for articles """

    template = 'blog/article_blog_page.html'

    subtitle = models.CharField(max_length=100, blank=True, null=True)

    intro_image = models.ForeignKey(
        'wagtailimages.Image',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        help_text='Best size for this image is 1400x400'
    )


    content_panels = Page.content_panels + [
        FieldPanel('custom_title'),
        FieldPanel('subtitle'),
        ImageChooserPanel('banner_image'),
        ImageChooserPanel('intro_image'),
        StreamFieldPanel('content'),
        MultiFieldPanel(
            [
                InlinePanel('blog_authors', label='Author', min_num=1, max_num=4)
            ],
            heading='Authors'
        ),
        MultiFieldPanel(
            [
                FieldPanel('categories', widget=forms.CheckboxSelectMultiple)
            ],
            heading='Categories'
        ), 
    ]


class VideoBlogPage(BlogDetailPage):
    """ A video subclassed page """

    youtube_video_id = models.CharField(max_length=50)

    content_panels = Page.content_panels + [
        FieldPanel('custom_title'),
        ImageChooserPanel('banner_image'),
        MultiFieldPanel(
            [
                InlinePanel('blog_authors', label='Author', min_num=1, max_num=4)
            ],
            heading='Author(s)'
        ),
        MultiFieldPanel(
            [
                FieldPanel('categories', widget=forms.CheckboxSelectMultiple)
            ],
            heading='Categories'
        ),
        FieldPanel('youtube_video_id'),
        StreamFieldPanel('content'),
    ]
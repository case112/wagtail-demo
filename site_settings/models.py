from django.db import models

from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel
from wagtail.contrib.settings.models import BaseSetting, register_setting

@register_setting
class SocialMediaSettings(BaseSetting):
    """ Social media settings for our custom website """

    facebook = models.URLField(blank=True, help_text='Facebook URL')
    instagram = models.URLField(blank=True, help_text='Instagram URL')
    github = models.URLField(blank=True, help_text='Github URL')

    panels = [
        MultiFieldPanel([
            FieldPanel('facebook'),
            FieldPanel('instagram'),
            FieldPanel('github'),
        ], heading='Social Meida Settings'),
    ]
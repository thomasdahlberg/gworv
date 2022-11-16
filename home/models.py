from django.db import models
from impact.models import ArticlePage
from about.models import Partner, IconLink

from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel
from wagtail.core.fields import RichTextField
from wagtail.core.models import Page
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.images.models import Image
from wagtail.snippets.models import register_snippet
from wagtail.snippets.edit_handlers import SnippetChooserPanel


class HomePage(Page):
    hero_header = models.CharField(max_length=250, blank=True, null=True)
    hero_subheader = models.TextField(blank=True, null=True)
    hero_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )
    hero_cta_text = models.CharField(max_length=250, blank=True, null=True)
    hero_cta_link = models.CharField(max_length=250, blank=True, null=True)

    mission_header = models.CharField(max_length=250, blank=True, null=True)
    mission_statement = models.TextField(blank=True, null=True)
    mission_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )
    mission_cta_text = models.CharField(max_length=250, blank=True, null=True)
    mission_cta_link = models.CharField(max_length=250, blank=True, null=True)

    impact_header = models.CharField(max_length=250, blank=True, null=True)
    impact_icon = models.CharField(max_length=250, blank=True, null=True)
    impact_cta_text = models.CharField(max_length=250, blank=True, null=True)
    impact_cta_link = models.CharField(max_length=250, blank=True, null=True)
    impact_primary_feature = models.ForeignKey(
        ArticlePage,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    impact_secondary_feature = models.ForeignKey(
        ArticlePage,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    impact_tertiary_feature = models.ForeignKey(
        ArticlePage,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    social_media_text = models.TextField(blank=True, null=True)

    involvement_header = models.CharField(
        max_length=250, blank=True, null=True)
    involvement_cta_link = models.CharField(
        max_length=250, blank=True, null=True)
    involvement_cta_text = models.CharField(
        max_length=250, blank=True, null=True)
    involvement_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    def get_context(self, request):
        context = super().get_context(request)
        partners = Partner.objects.filter(
            active=True)
        # social_media_links = IconLink.objects.filter(
        #     active=True, partner_name="groundwork_over"
        # )
        context['partners'] = partners
        # context['social_media_links'] = social_media_links
        return context

    content_panels = Page.content_panels + [
        FieldPanel('hero_header'),
        FieldPanel('hero_subheader'),
        FieldPanel('hero_image'),
        FieldPanel('hero_cta_text'),
        FieldPanel('hero_cta_link'),
        FieldPanel('mission_header'),
        FieldPanel('mission_statement'),
        FieldPanel('mission_image'),
        FieldPanel('mission_cta_text'),
        FieldPanel('mission_cta_link'),
        FieldPanel('impact_header'),
        FieldPanel('impact_icon'),
        FieldPanel('impact_cta_text'),
        FieldPanel('impact_cta_link'),
        FieldPanel('impact_primary_feature'),
        FieldPanel('impact_secondary_feature'),
        FieldPanel('impact_tertiary_feature'),
        FieldPanel('social_media_text'),
        FieldPanel('involvement_header'),
        FieldPanel('involvement_image'),
        FieldPanel('involvement_cta_text'),
        FieldPanel('involvement_cta_link'),
    ]

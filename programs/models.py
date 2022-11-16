from django.db import models
from involvement.models import JobPosting

from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel


from wagtail.snippets.models import register_snippet

CITIZEN_SCI = 'cts'
GREEN_WORK = 'gwf'
CLIMATE_SAFE = 'csn'


@register_snippet
class ImpactDataCard(models.Model):
    figure = models.CharField(max_length=250, blank=True, null=True)
    unit = models.CharField(max_length=250, blank=True, null=True)
    description = models.CharField(max_length=250, blank=True, null=True)
    active = models.BooleanField(default=True)
    # add badge when clarified with design

    panels = [
        FieldPanel('figure'),
        FieldPanel('unit'),
        FieldPanel('description'),
        FieldPanel('active'),
    ]


@register_snippet
class Program(models.Model):
    TYPE_CHOICES = [
        (CITIZEN_SCI, 'Citizen Scientist'),
        (GREEN_WORK, 'Green Workforce'),
        (CLIMATE_SAFE, 'Climate Safe Neighborhood'),
    ]
    name = models.CharField(max_length=250, blank=True, null=True)
    description = RichTextField(blank=True)
    category = models.CharField(
        max_length=3,
        choices=TYPE_CHOICES,
        default=GREEN_WORK,
    )
    cta_text = models.CharField(max_length=250, blank=True, null=True)
    cta_link = models.CharField(max_length=250, blank=True, null=True)
    active = models.BooleanField(default=True)

    panels = [
        FieldPanel('name'),
        FieldPanel('description'),
        FieldPanel('category'),
        FieldPanel('cta_text'),
        FieldPanel('cta_link'),
        FieldPanel('active'),
    ]


class ProgramsIndexPage(Page):
    hero_header = models.CharField(max_length=250, blank=True, null=True)
    hero_description = models.TextField(blank=True, null=True)
    hero_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    impact_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )
    impact_cta_text = models.CharField(max_length=250, blank=True, null=True)
    impact_cta_link = models.CharField(max_length=250, blank=True, null=True)
    # figure out how icons and badges work for impact_icon

    work_header = models.CharField(max_length=250, blank=True, null=True)

    involvement_header = RichTextField(blank=True)
    involvement_cta_text = models.CharField(
        max_length=250, blank=True, null=True)
    involvement_cta_link = models.CharField(
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
        child_pages = self.get_children().live()
        programs = Program.objects.filter(
            active=True)
        impact_cards = ImpactDataCard.objects.filter(
            active=True)
        job_opportunities = JobPosting.objects.filter(
            active=True)
        context['child_pages'] = child_pages
        context['programs'] = programs
        context['impact_cards'] = impact_cards
        context['job_opportunities'] = job_opportunities
        return context

    content_panels = Page.content_panels + [
        FieldPanel('hero_header'),
        FieldPanel('hero_description'),
        FieldPanel('hero_image'),
        FieldPanel('impact_image'),
        FieldPanel('impact_cta_text'),
        FieldPanel('impact_cta_link'),
        FieldPanel('work_header'),
        FieldPanel('involvement_header'),
        FieldPanel('involvement_cta_text'),
        FieldPanel('involvement_cta_link'),
        FieldPanel('involvement_image'),
    ]


class ProgramPage(Page):
    hero_header = models.CharField(max_length=250, blank=True, null=True)
    hero_header_icon = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )
    hero_description = RichTextField(blank=True)
    hero_cta_text = models.CharField(max_length=250, blank=True, null=True)
    hero_cta_link = models.CharField(max_length=250, blank=True, null=True)
    hero_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )
    hero_badge = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    badge_header = models.CharField(max_length=250, blank=True, null=True)
    # TODO: add badges solution here

    secondary_header = models.CharField(max_length=250, blank=True, null=True)
    secondary_hero_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    # this appears on the button in each of the article blurbs
    article_cta_text = models.CharField(max_length=250, blank=True, null=True)

    work_opportunity_header = models.CharField(
        max_length=250, blank=True, null=True)

    volunteer_badge = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )
    volunteer_header = models.CharField(
        max_length=250, blank=True, null=True)
    volunteer_description = RichTextField(blank=True)

    def get_context(self, request):
        context = super().get_context(request)
        # add category criteria to jobs filter below when that is decided
        job_opportunities = JobPosting.objects.filter(
            active=True)
        context['job_opportunities'] = job_opportunities
        return context

    content_panels = Page.content_panels + [
        FieldPanel('hero_header'),
        FieldPanel('hero_header_icon'),
        FieldPanel('hero_description'),
        FieldPanel('hero_image'),
        FieldPanel('hero_cta_text'),
        FieldPanel('hero_cta_link'),
        FieldPanel('hero_image'),
        FieldPanel('hero_badge'),
        FieldPanel('badge_header'),
        FieldPanel('secondary_header'),
        FieldPanel('secondary_hero_image'),
        FieldPanel('article_cta_text'),
        FieldPanel('work_opportunity_header'),
        FieldPanel('volunteer_header'),
        FieldPanel('volunteer_description'),
        FieldPanel('volunteer_badge'),
    ]

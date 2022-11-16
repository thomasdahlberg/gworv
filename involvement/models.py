from django.db import models

from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel

from wagtail.snippets.models import register_snippet


@register_snippet
class JobPosting(models.Model):
    name = models.CharField(blank=True, max_length=250)
    description = RichTextField(blank=True)
    link = models.CharField(blank=True, max_length=250)
    active = models.BooleanField(default=True)
    category = models.CharField(blank=True, max_length=250)
    # TODO: Find out if groundwork wants to categorize jobs
    # TODO: Find out how groundwork plans to serve PDFs of job postings

    panels = [
        FieldPanel('name'),
        FieldPanel('description'),
        FieldPanel('link'),
        FieldPanel('active'),
        FieldPanel('category'),
    ]


class GetInvolvedIndexPage(Page):
    hero_header = models.CharField(max_length=250, blank=True, null=True)
    hero_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )
    volunteer_header = models.CharField(max_length=250, blank=True, null=True)
    volunteer_description = RichTextField(blank=True)
    hiring_header = models.CharField(max_length=250, blank=True, null=True)
    hiring_button_text = models.CharField(
        max_length=250, blank=True, null=True)
    stay_involved_header = models.CharField(
        max_length=250, blank=True, null=True)
    stay_involved_description = RichTextField(blank=True)

    def get_context(self, request):
        context = super().get_context(request)
        job_opportunities = JobPosting.objects.filter(
            active=True)
        context['job_opportunities'] = job_opportunities
        return context

    content_panels = Page.content_panels + [
        FieldPanel('hero_header'),
        ImageChooserPanel('hero_image'),
        FieldPanel('volunteer_header'),
        FieldPanel('volunteer_description'),
        FieldPanel('hiring_header'),
        FieldPanel('hiring_button_text'),
        FieldPanel('stay_involved_header'),
        FieldPanel('stay_involved_description'),
    ]

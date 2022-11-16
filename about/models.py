from django.db import models

from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel
from wagtail.snippets.models import register_snippet
from wagtail.images.edit_handlers import ImageChooserPanel

BOARD_MEMBER = 'BM'
EMPLOYEE = 'EMP'
DIRECTOR = 'DIR'
YOU_TUBE = 'YT'
INSTAGRAM = 'IG'
FACEBOOK = 'FB'


@register_snippet
class Bio(models.Model):
    TYPE_CHOICES = [
        (BOARD_MEMBER, 'Board Member'),
        (EMPLOYEE, 'Employee'),
        (DIRECTOR, 'Director'),
    ]
    first_name = models.CharField(max_length=250, blank=True, null=True)
    last_name = models.CharField(max_length=250, blank=True, null=True)
    role = models.CharField(max_length=250)
    email = models.EmailField(max_length=200)
    bio_text = models.TextField(blank=True, null=True)
    type = models.CharField(
        max_length=3,
        choices=TYPE_CHOICES,
        default=EMPLOYEE,
    )
    avatar = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
    )
    active = models.BooleanField(default=True)
    affiliation = models.CharField(max_length=250, blank=True, null=True)

    def is_board_member(self):
        return self.type == self.BOARD_MEMBER

    def is_director(self):
        return self.type == self.DIRECTOR

    def is_staff(self):
        return self.type == self.STAFF

    panels = [
        FieldPanel('first_name'),
        FieldPanel('last_name'),
        FieldPanel('role'),
        FieldPanel('email'),
        FieldPanel('bio_text'),
        FieldPanel('type'),
        ImageChooserPanel('avatar'),
        FieldPanel('affiliation'),
        FieldPanel('active'),
    ]

    def __str__(self):
        return f"{self.last_name}, {self.first_name} - {self.role}"


@register_snippet
class Partner(models.Model):
    name = models.CharField(max_length=250, blank=True, null=True)
    avatar = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
    )
    active = models.BooleanField(default=True)
    panels = [
        FieldPanel('name'),
        ImageChooserPanel('avatar'),
        FieldPanel('active'),
    ]


@register_snippet
class IconLink(models.Model):
    # TODO: decide if we want the Icons themselves to be a model so that Groundwork
    # and add them as new link types emerge into fashion (i.e tiktok, etc)
    TYPE_CHOICES = [
        (YOU_TUBE, 'YouTube'),
        (INSTAGRAM, 'Instagram'),
        (FACEBOOK, 'Facebook'),
    ]
    # label used as aria-label for a11y
    label = models.CharField(max_length=200)
    url = models.CharField(max_length=200)
    partner_name = models.ForeignKey(Partner, on_delete=models.CASCADE)
    type = models.CharField(
        max_length=2,
        choices=TYPE_CHOICES,
        default=INSTAGRAM,
    )
    active = models.BooleanField(default=True)
    panels = [
        FieldPanel('partner_name'),
        FieldPanel('active'),
        FieldPanel('url'),
        FieldPanel('type'),
    ]


class AboutIndexPage(Page):
    # splash text and image need to be ironed out with design
    splash_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )
    splash_text = models.TextField(blank=True, null=True)

    mission_header = models.CharField(max_length=250, blank=True, null=True)
    mission_text = models.TextField(blank=True, null=True)

    images = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )
    # need clarification from design if this is an iframe of youtube
    video_url = models.CharField(max_length=500, blank=True, null=True)

    team_header = RichTextField(blank=True)
    partners_header = RichTextField(blank=True)
    team_directors_subheader = models.CharField(
        max_length=250, blank=True, null=True)
    team_board_subheader = models.CharField(
        max_length=250, blank=True, null=True)
    team_staff_subheader = models.CharField(
        max_length=250, blank=True, null=True)

    def get_context(self, request):
        context = super().get_context(request)
        context['child_pages'] = self.get_children().live()
        context['director_bios'] = Bio.objects.filter(
            type=DIRECTOR, active=True)
        context['board_bios'] = Bio.objects.filter(
            type=BOARD_MEMBER, active=True)
        context['staff_bios'] = Bio.objects.filter(
            type=EMPLOYEE, active=True)
        return context

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                ImageChooserPanel('splash_image'),
                FieldPanel('splash_text'),
                FieldPanel('mission_header'),
                FieldPanel('mission_text'),
                ImageChooserPanel('images'),
                FieldPanel('video_url'),
            ],
            heading="Mission Section Settings",
        ),
        MultiFieldPanel(
            [
                FieldPanel('team_header'),
                FieldPanel('partners_header'),
                FieldPanel('team_directors_subheader'),
                FieldPanel('team_board_subheader'),
                FieldPanel('team_staff_subheader'),
            ],
            heading="Team Section Settings",
        ),
    ]

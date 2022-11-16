from django import forms
from django.db import models

from modelcluster.fields import ParentalKey, ParentalManyToManyField
# from taggit.models import TaggedItemBase, Tag
# from modelcluster.contrib.taggit import ClusterTaggableManager

from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel
# from wagtail.search import index

from wagtail.snippets.models import register_snippet


@register_snippet
class NewsCategory(models.Model):
    name = models.CharField(max_length=255)
    icon = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='+'
    )

    panels = [
        FieldPanel('name'),
        FieldPanel('icon'),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'news categories'


class ArticlePage(Page):
    splash_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )
    published_date = models.DateField("Post date")
    body = RichTextField(blank=True)
    # tags = ClusterTaggableManager(through=ArticlePageTag, blank=True)
    category = models.ForeignKey(NewsCategory, on_delete=models.PROTECT)
    back_button_text = models.CharField(max_length=250, blank=True, null=True)
    back_button_link = models.CharField(max_length=250, blank=True, null=True)
    blurb = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('category'),
        ], heading="News Article Information"),
        FieldPanel('body', classname="full"),
        InlinePanel('gallery_images', label="Gallery images"),
    ]


class ArticleGalleryImage(Orderable):
    page = ParentalKey(ArticlePage, on_delete=models.CASCADE,
                       related_name='gallery_images')
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )
    caption = models.CharField(blank=True, max_length=250)

    panels = [
        FieldPanel('image'),
        FieldPanel('caption'),
    ]


class Impact(Page):
    header = models.CharField(max_length=250, blank=True, null=True)
    more_button_text = models.CharField(max_length=250, blank=True, null=True)
    primary_feature = models.ForeignKey(
        ArticlePage,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    secondary_feature = models.ForeignKey(
        ArticlePage,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    tertiary_feature = models.ForeignKey(
        ArticlePage,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    def get_context(self, request):
        context = super().get_context(request)
        categories = NewsCategory.objects.all()
        # tags = Tag.objects.all()
        articles = self.get_children().live().order_by('-first_published_at')
        context['categories'] = categories
        # context['tags'] = tags
        context['articles'] = articles
        return context

    content_panels = Page.content_panels + [
        FieldPanel('header', classname="full"),
        FieldPanel('more_button_text', classname="full"),
        FieldPanel('primary_feature'),
        FieldPanel('secondary_feature'),
        FieldPanel('tertiary_feature')
    ]


# class ArticlePageTag(TaggedItemBase):
#     content_object = ParentalKey(
#         'NewsArticlePage',
#         related_name='tagged_items',
#         on_delete=models.CASCADE
#     )


# class ArticleTagIndexPage(Page):

#     def get_context(self, request):

#         # Filter by tag
#         category_id = None
#         tag = request.GET.get('tag', None)
#         category_name = request.GET.get('category', None)

#         if category_name:
#             try:
#                 category_id = NewsCategory.objects.get(name=category_name)
#             except:
#                 category_id = None
#         if tag == 'all':
#             print('*************** ALL ARTICLES ***********')
#             articles = NewsArticlePage.objects.all()
#         elif category_id and tag:
#             print('***************** BOTH CAT AND TAG *******')
#             articles = NewsArticlePage.objects.filter(
#                 tags__name=tag, categories=category_id)
#         elif category_id:
#             print('****************** CATEGORY ***********')
#             articles = NewsArticlePage.objects.filter(categories=category_id)
#         elif tag:
#             print('****************** TAG ***********')
#             articles = NewsArticlePage.objects.filter(tags__name=tag)
#         else:
#             articles = None

#         # Update template context
#         context = super().get_context(request)
#         context['articles'] = articles
#         return context

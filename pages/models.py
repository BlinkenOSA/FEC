from __future__ import absolute_import, unicode_literals

from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.wagtailadmin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailforms.models import AbstractFormField, AbstractEmailForm
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from condensedinlinepanel.edit_handlers import CondensedInlinePanel
from wagtailcaptcha.models import WagtailCaptchaEmailForm


class HomePage(Page):
    hero_video_url = models.CharField(max_length=100)
    hero_text_top = models.CharField(max_length=100, blank=True)
    hero_text_title = models.CharField(max_length=100)
    hero_text_motto = models.CharField(max_length=100, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('hero_video_url'),
        FieldPanel('hero_text_top'),
        FieldPanel('hero_text_title'),
        FieldPanel('hero_text_motto'),
        CondensedInlinePanel('counters', label="Counters", card_header_from_field="counter_text"),
        CondensedInlinePanel('badges', label="Badges", card_header_from_field="badge_header_text")
    ]

    def get_context(self, request, *args, **kwargs):
        context = super(HomePage, self).get_context(request)
        context['counter_blocks'] = self.counters.all()
        context['counter_blocks_count'] = self.counters.count()
        context['badge_blocks'] = self.badges.all()
        context['badge_blocks_count'] = self.badges.count()
        return context


class HomePageCounter(Orderable):
    page = ParentalKey('HomePage', related_name='counters', blank=True, null=True)
    counter = models.IntegerField()
    counter_text = models.CharField(max_length=50)

    panels = [
        FieldPanel('counter'),
        FieldPanel('counter_text'),
    ]


class HomePageBadgePanel(Orderable):
    page = ParentalKey('HomePage', related_name='badges', blank=True, null=True)
    url = models.CharField(max_length=40)
    badge_icon_class = models.CharField(max_length=20)
    badge_header_text = models.CharField(max_length=50)
    badge_description = models.CharField(max_length=200)

    panels = [
        FieldPanel('url'),
        FieldPanel('badge_icon_class'),
        FieldPanel('badge_header_text'),
        FieldPanel('badge_description')
    ]


class FaqPage(Page):
    header_image = models.ForeignKey('wagtailimages.Image', related_name='+', on_delete=models.PROTECT)
    body_title = models.CharField(max_length=100, blank=True, null=True)
    body_text = RichTextField(blank=True, null=True)

    content_panels = Page.content_panels + [
        ImageChooserPanel('header_image'),
        FieldPanel('body_title'),
        FieldPanel('body_text', classname='full'),
        CondensedInlinePanel('faq_items', label='FAQ Items', card_header_from_field='question')
    ]

    def get_context(self, request, *args, **kwargs):
        context = super(FaqPage, self).get_context(request)
        context['faq_blocks'] = self.faq_items.all()
        context['faq_blocks_count'] = self.faq_items.count()
        return context


class FaqPageItem(Orderable):
    page = ParentalKey('FaqPage', related_name='faq_items', blank=True, null=True)
    question = models.CharField(max_length=150)
    answer = RichTextField()

    panels = [
        FieldPanel('question'),
        FieldPanel('answer', classname='full')
    ]


class TimelinePage(Page):
    header_image = models.ForeignKey('wagtailimages.Image', related_name='+', on_delete=models.PROTECT)

    content_panels = Page.content_panels + [
        ImageChooserPanel('header_image'),
        CondensedInlinePanel('timeline_items', label='Timeline Items', card_header_from_field='title')
    ]

    def get_context(self, request, *args, **kwargs):
        context = super(TimelinePage, self).get_context(request)
        context['timeline_blocks'] = self.timeline_items.all()
        return context


class TimelinePageItem(Orderable):
    page = ParentalKey('TimelinePage', related_name='timeline_items', blank=True, null=True)
    header_image = models.ForeignKey('wagtailimages.Image', related_name='+', on_delete=models.PROTECT, blank=True, null=True)
    date = models.DateField()
    title = models.CharField(max_length=150)
    body = RichTextField()

    panels = [
        ImageChooserPanel('header_image'),
        FieldPanel('date'),
        FieldPanel('title'),
        FieldPanel('body', classname='full')
    ]


class ContactFormField(AbstractFormField):
    page = ParentalKey('ContactFormPage', related_name='form_fields')


class ContactFormPage(WagtailCaptchaEmailForm):
    header_image = models.ForeignKey('wagtailimages.Image', related_name='+',
                                     on_delete=models.PROTECT, blank=True, null=True)
    body = RichTextField(blank=True, help_text='Edit the content you want to see before the form.')
    thank_you_text = RichTextField(blank=True, help_text='Set the message users will see after submitting the form.')

    content_panels = [
        ImageChooserPanel('header_image'),
        FieldPanel('title', classname="full title"),
        FieldPanel('body', classname="full"),
        FieldPanel('thank_you_text', classname="full"),
        InlinePanel('form_fields', label="Form fields"),
        MultiFieldPanel([
            FieldPanel('to_address'),
            FieldPanel('from_address'),
            FieldPanel('subject'),
        ], "Email notification")
    ]
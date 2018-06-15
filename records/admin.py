from django.contrib import admin
from django.contrib.admin import ModelAdmin, StackedInline, TabularInline
from tabbed_admin import TabbedModelAdmin

from records.models import FECEntity, AssociatedPerson, Country, Corporation, Person


class AssociatedPersonInline(TabularInline):
    model = AssociatedPerson
    extra = 1
    verbose_name = 'Associated Person'
    verbose_name_plural = 'Associated People'
    fields = (('role', 'person'))

    raw_id_fields = ('person',)
    autocomplete_lookup_fields = {
        'fk': ['person']
    }


class FECEntityAdmin(TabbedModelAdmin):
    model = FECEntity
    list_display = ('title', 'date', 'doc_name')
    list_display_link = ('title',)
    date_hierarchy = 'date'
    ordering = ('date', 'title')
    list_filter = ('place', 'countries', 'associated_people__person', 'subject_corporations__corporation')

    raw_id_fields = ('countries', 'subject_people', 'subject_corporations', 'associated_corporations')
    autocomplete_lookup_fields = {
        'm2m': ['countries', 'subject_people', 'subject_corporations', 'associated_corporations']
    }

    tab_general = (
        (None, {
            'fields': ('doc_name', 'title', 'title_given', 'date', 'place', 'pages', 'confidential', 'is_coded',
                       'is_handwritten', 'summary', 'note', 'internal_note')
        }),
    )

    tab_contributors = (
        AssociatedPersonInline,
        ('Associated Corporations', {
            'fields': ('associated_corporations',)
        })
    )

    tab_subjects = (
        (None, {
            'fields': ('countries', 'subject_people', 'subject_corporations')
        }),
    )

    tabs = [
        ('General', tab_general),
        ('Contributors', tab_contributors),
        ('Subjects', tab_subjects)
    ]


class CountryAdmin(admin.ModelAdmin):
    model = Country
    ordering = ('country',)


class PersonAdmin(admin.ModelAdmin):
    model = Person
    ordering = ('person',)


class CorporationAdmin(admin.ModelAdmin):
    model = Person
    ordering = ('corporation',)


admin.site.register(FECEntity, FECEntityAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(Corporation, CorporationAdmin)
admin.site.register(Person, PersonAdmin)


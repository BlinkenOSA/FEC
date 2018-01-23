from django.contrib import admin
from django.contrib.admin import ModelAdmin

from records.models import FECEntity


class FECEntityAdmin(ModelAdmin):
    list_display = ('title', 'date', 'doc_name')
    list_display_link = ('title',)
    date_hierarchy = 'date'
    ordering = ('date', 'title')
    list_filter = ('place', 'countries')
    filter_horizontal = ['associated_people', 'associated_corporations', 'countries',
                         'subject_people', 'subject_corporations']

admin.site.register(FECEntity, FECEntityAdmin)


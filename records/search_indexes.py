import urllib

from haystack import indexes

from records.models import FECEntity


class RecordIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    date = indexes.DateField(indexed=True, model_attr="date")
    title_display = indexes.CharField(indexed=False, stored=True, model_attr='title')
    date_display = indexes.CharField(indexed=False, stored=True, model_attr='date')
    place_display = indexes.CharField(indexed=False, stored=True)
    doc_id = indexes.CharField(indexed=False, stored=True, model_attr='doc_name')

    # Facets
    place = indexes.CharField(null=True, faceted=True)
    associated_people = indexes.MultiValueField(null=True, faceted=True)
    associated_corporations = indexes.MultiValueField(null=True, faceted=True)
    countries = indexes.MultiValueField(null=True, faceted=True)
    subject_people = indexes.MultiValueField(null=True, faceted=True)
    subject_corporations = indexes.MultiValueField(null=True, faceted=True)

    def get_model(self):
        return FECEntity

    def prepare_associated_people(self, obj):
        values = []
        for ap in obj.associated_people.all():
            values.append(ap.person)
        return values

    def prepare_associated_corporations(self, obj):
        values = []
        for ac in obj.associated_corporations.all():
            values.append(ac.corporation)
        return values

    def prepare_subject_people(self, obj):
        values = []
        for sp in obj.subject_people.all():
            values.append(sp.person)
        return values

    def prepare_subject_corporations(self, obj):
        values = []
        for sc in obj.subject_corporations.all():
            values.append(sc.corporation)
        return values

    def prepare_countries(self, obj):
        values = []
        for c in obj.countries.all():
            values.append(c.country)
        return values

    def prepare_place(self, obj):
        return obj.place.place

    def prepare_place_display(self, obj):
        return obj.place.place

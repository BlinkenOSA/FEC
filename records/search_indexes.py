import urllib

from haystack import indexes

from records.models import FECEntity


class RecordIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    date = indexes.CharField(indexed=True, model_attr="date")
    title_display = indexes.CharField(indexed=False, stored=True, model_attr='title')
    date_display = indexes.CharField(indexed=False, stored=True, model_attr='date')
    place_display = indexes.CharField(indexed=False, stored=True)
    doc_id = indexes.CharField(indexed=False, stored=True, model_attr='doc_name')

    # Facets
    place = indexes.FacetCharField(null=True)
    associated_people = indexes.FacetMultiValueField(null=True)
    associated_corporations = indexes.FacetMultiValueField(null=True)
    countries = indexes.FacetMultiValueField(null=True)
    subject_people = indexes.FacetMultiValueField(null=True)
    subject_corporations = indexes.FacetMultiValueField(null=True)

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

    def prepare_doc_id(self, obj):
        return urllib.quote_plus("fec/%s/%s_%s.jpg" % (obj.doc_name[:2],
                                                       obj.doc_name[:2],
                                                       str(obj.doc_name[3:])))

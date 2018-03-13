from django import forms
from django.forms import HiddenInput
from haystack.forms import FacetedSearchForm


class DateRangeSearchForm(FacetedSearchForm):
    start_date = forms.DateField(required=False, widget=HiddenInput())
    end_date = forms.DateField(required=False, widget=HiddenInput())
    facets = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        super(DateRangeSearchForm, self).__init__(*args, **kwargs)
        self.selected_facets = []

        self.selected_facets.extend(self.get_facet('associated_people', **kwargs))
        self.selected_facets.extend(self.get_facet('subject_people', **kwargs))
        self.selected_facets.extend(self.get_facet('subject_corporations', **kwargs))
        self.selected_facets.extend(self.get_facet('countries', **kwargs))
        self.selected_facets.extend(self.get_facet('place', **kwargs))


    def get_facet(self, facet_name, **kwargs):
        facets = kwargs['data'].getlist(facet_name, [])
        return list(map(lambda x: "%s:%s" % (facet_name, x), facets))

    def search(self):
        # First, store the SearchQuerySet received from other processing.
        sqs = super(DateRangeSearchForm, self).search()

        if not self.is_valid():
            return self.no_query_found()

        # Check to see if a start_date was chosen.
        if self.cleaned_data['start_date']:
            sqs = sqs.filter(date__gte=self.cleaned_data['start_date'])

        # Check to see if an end_date was chosen.
        if self.cleaned_data['end_date']:
            sqs = sqs.filter(date__lte=self.cleaned_data['end_date'])

        # We need to process each facet to ensure that the field name and the
        # value are quoted correctly and separately:
        for facet in self.selected_facets:
            if ":" not in facet:
                continue

            field, value = facet.split(":", 1)

            if value:
                sqs = sqs.narrow(u'%s:"%s"' % (field, sqs.query.clean(value)))

        sqs = sqs.facet('associated_people', limit=-1, sort='count', mincount=1)
        sqs = sqs.facet('countries', limit=-1, sort='count', mincount=1)
        sqs = sqs.facet('subject_people', limit=-1, sort='count', mincount=1)
        sqs = sqs.facet('subject_corporations', limit=-1, sort='count', mincount=1)
        sqs = sqs.facet('place', limit=-1, sort='count', mincount=1)

        return sqs.order_by('date_display', 'title_display')

    def no_query_found(self):
        """
        Return all results for search queries with no parameter
        """
        return self.searchqueryset.all()

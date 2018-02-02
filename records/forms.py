from django import forms
from haystack.forms import FacetedSearchForm


class DateRangeSearchForm(FacetedSearchForm):
    start_date = forms.DateField(required=False)
    end_date = forms.DateField(required=False)

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

        return sqs.order_by('date_display', 'title_display')

    def no_query_found(self):
        """
        Return all results for search queries with no parameter
        """
        return self.searchqueryset.all()

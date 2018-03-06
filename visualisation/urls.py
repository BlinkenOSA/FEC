from django.conf.urls import url

from visualisation.views import VisualisationView, GraphView

urlpatterns = [
    url(r'^vis/?$', VisualisationView.as_view(), name='chart'),
    url(r'^graph/?$', GraphView.as_view(), name='graph')
]
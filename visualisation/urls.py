from django.conf.urls import url

from visualisation.views import VisualisationView

urlpatterns = [
    url(r'^vis/?$', VisualisationView.as_view(), name='chart')
]
from django.conf.urls import url
from records.views import EntityDetailView, EntityManifestView, EntitySearchView

urlpatterns = [
    url(r'^(?P<pk>\d+)/$', EntityDetailView.as_view(), name='view'),
    url(r'^search/?$', EntitySearchView.as_view(), name='search'),
    url(r'^manifest/(?P<pk>\d+)/$', EntityManifestView.as_view(), name='manifest'),
]
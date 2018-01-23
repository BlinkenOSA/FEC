from django.conf.urls import url
from records.views import EntityDetailView, EntityManifestView

urlpatterns = [
    url(r'^(?P<pk>\d+)/$', EntityDetailView.as_view(), name='view'),
    url(r'^manifest/(?P<pk>\d+)/$', EntityManifestView.as_view(), name='manifest'),
]
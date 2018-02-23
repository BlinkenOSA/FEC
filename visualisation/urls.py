from django.conf.urls import url
from records.views import EntitySearchView

urlpatterns = [
    url(r'^message_number/?$', EntitySearchView.as_view(), name='search'),
]
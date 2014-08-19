from django.conf.urls import patterns, url

from .views import StatusIndex

urlpatterns = patterns(
    '',

    url(r'^$', StatusIndex.as_view(), name='status-index'),
)

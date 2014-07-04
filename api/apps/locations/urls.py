from django.conf.urls import patterns, url

from .views import LocationList, LocationDetail

urlpatterns = patterns(
    '',

    url(r'^$',
        LocationList.as_view(),
        name='location-list'),

    url(r'^(?P<slug>[a-z0-9-]+)/$',
        LocationDetail.as_view(),
        name='location-detail'),
)

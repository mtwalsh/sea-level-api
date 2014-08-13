from django.conf.urls import patterns, url
from django.conf import settings

from .views import SeaLevels, SeaLevelsNow

urlpatterns = patterns(
    '',

    url(r'^$', SeaLevels.as_view(), name='sea-levels'),

    url(r'^(?P<location_slug>' + settings.SLUG_REGEX + ')/$',
        SeaLevels.as_view(),
        name='sea-levels'),

    url(r'^(?P<location_slug>' + settings.SLUG_REGEX + ')/now/$',
        SeaLevelsNow.as_view(),
        name='sea-levels'),
)

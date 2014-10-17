from django.conf.urls import patterns, url
from django.conf import settings

from .views import (
    TideLevels, TideLevelsNow, TideWindows, TideWindowsNow, SurgeLevels)

urlpatterns = patterns(
    '',

    url(r'^tide-levels/$', TideLevels.as_view(), name='tide-levels'),
    url(r'^tide-windows/$', TideWindows.as_view(), name='tide-windows'),

    url(r'^tide-levels/(?P<location_slug>' + settings.SLUG_REGEX + ')/$',
        TideLevels.as_view(),
        name='tide-levels'),

    url(r'^surge-levels/(?P<location_slug>' + settings.SLUG_REGEX + ')/$',
        SurgeLevels.as_view(),
        name='surge-levels'),

    url(r'^tide-levels/(?P<location_slug>' + settings.SLUG_REGEX + ')/now/$',
        TideLevelsNow.as_view(),
        name='tide-levels'),

    url(r'^tide-windows/(?P<location_slug>' + settings.SLUG_REGEX + ')/$',
        TideWindows.as_view(),
        name='tide-windows'),

    url(r'^tide-windows/(?P<location_slug>' + settings.SLUG_REGEX + ')/now/$',
        TideWindowsNow.as_view(),
        name='tide-windows'),
)

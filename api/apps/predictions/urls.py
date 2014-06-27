from django.conf.urls import patterns, url

from views import TideLevels, TideWindows

SLUG_REGEX = '[a-z0-9-]+'
DATETIME_REGEX = '\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z'

urlpatterns = patterns(
    '',

    url(r'^tide-levels/$', TideLevels.as_view(), name='tide-levels'),
    url(r'^tide-windows/$', TideWindows.as_view(), name='tide-windows'),

    url(r'^tide-levels/(?P<location_slug>' + SLUG_REGEX + ')/$',
        TideLevels.as_view(),
        name='tide-levels'),

    url(r'^tide-windows/(?P<location_slug>' + SLUG_REGEX + ')/$',
        TideWindows.as_view(),
        name='tide-windows'),
)

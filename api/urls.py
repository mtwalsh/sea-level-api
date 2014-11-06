from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic.base import RedirectView

from .api_root_view import ApiRoot

urlpatterns = [
    # Examples:
    # url(r'^$', 'api.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', RedirectView.as_view(url='/1/', permanent=False)),

    url(r'^1/$', ApiRoot.as_view(), name='api-root'),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^1/locations/', include('api.apps.locations.urls')),
    url(r'^1/predictions/', include('api.apps.predictions.urls')),

    url(r'^1/sea-levels/', include('api.apps.sea_levels.urls')),

    url(r'^1/tide-gauges/', include('api.apps.tide_gauges.urls')),

    url(r'^1/_status/', include('api.apps.status.urls')),
]

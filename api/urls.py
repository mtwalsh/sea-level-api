from django.conf.urls import include, url
from django.contrib import admin

from .api_root_view import ApiRoot

urlpatterns = [
    # Examples:
    # url(r'^$', 'api.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', ApiRoot.as_view()),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^1/locations/', include('api.apps.locations.urls')),
    url(r'^1/predictions/', include('api.apps.predictions.urls')),
]

from django.conf.urls import url

from .views.predictions import predictions_view, predictions_redirect_now


urlpatterns = [
    url(r'now', predictions_redirect_now),
    url(r'', predictions_view),
]

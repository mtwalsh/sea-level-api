from rest_framework import generics
from rest_framework.response import Response
from rest_framework.reverse import reverse


class ApiRoot(generics.GenericAPIView):
    def get(self, req, format=None):
        return Response({
            'links': [
                {'href': reverse('location-list', request=req, format=format)},
                {'href': reverse('tide-levels', request=req, format=format)},
                {'href': reverse('tide-windows', request=req, format=format)},
            ]
        })

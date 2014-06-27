from rest_framework import generics
from rest_framework.response import Response
from rest_framework.reverse import reverse


class ApiRoot(generics.GenericAPIView):
    def get(self, request, format=None):
        return Response({
            'links': [
                reverse('location-list', request=request, format=format),
                reverse('tide-levels', request=request, format=format),
                reverse('tide-windows', request=request, format=format),
            ]
        })

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.reverse import reverse


class ApiRoot(generics.GenericAPIView):
    def get(self, request, format=None):
        return Response({
            'locations': reverse('location-list',
                                 request=request,
                                 format=format),

            'predictions': reverse('prediction-list',
                                   request=request,
                                   format=format),
        })

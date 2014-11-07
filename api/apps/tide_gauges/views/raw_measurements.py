from rest_framework.exceptions import APIException
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly
from rest_framework.response import Response
from rest_framework import status

from ..serializers import RawMeasurementListSerializer
from ..models import RawMeasurement, TideGauge


class InvalidDataError(APIException):
    status_code = 400


class RawMeasurements(GenericAPIView):
    """
    Store raw measurements for a tide gauge. Predictions must be given in a
    JSON array. Note that any bad prediction in the list will cause the
    entire batch to be dropped.
    """

    permission_classes = (DjangoModelPermissionsOrAnonReadOnly,)
    queryset = RawMeasurement.objects.none()  # req for DjangoModelPermissions

    def post(self, request, *args, **kwargs):
        tide_gauge = TideGauge.objects.get(slug=self.kwargs['tide_gauge_slug'])

        serializer = RawMeasurementListSerializer(data=request.data)

        if not serializer.is_valid():
            raise InvalidDataError(serializer.errors)
        serializer.save(tide_gauge=tide_gauge)

        return Response({'detail': 'OK.'}, status=status.HTTP_200_OK)

    def get_serializer(self, instance=None, data=None):
        # This is used to work out the endpoint's metadata, ie what fields it
        # supports and so on.
        assert instance is None and data is None, (
            'instance={}, data={}'.format(instance, data))

        # TODO: Remove this workaround once this bug is fixed:
        # https://github.com/tomchristie/django-rest-framework/issues/2035
        return RawMeasurementListSerializer.child

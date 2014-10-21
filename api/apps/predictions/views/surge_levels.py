from django.db import transaction

from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly
from rest_framework.response import Response

from api.apps.locations.models import Location

from ..models import SurgePrediction
from ..serializers import SurgeLevelSerializer


class JsonFormatError(APIException):
    status_code = 400


class InvalidDataError(APIException):
    status_code = 400


class SurgeLevels(GenericAPIView):
    """
    Store surge level predictions for the given location. Predictions must be
    given in a JSON array. Note that any bad prediction in the list will
    cause the entire batch to be dropped.
    """
    permission_classes = (DjangoModelPermissionsOrAnonReadOnly,)
    queryset = SurgePrediction.objects.none()  # Req for DjangoModelPermissions

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        location = Location.objects.get(slug=self.kwargs['location_slug'])

        context = {'request': request}

        if not isinstance(request.data, list):
            raise JsonFormatError('Data must be inside a JSON array eg []')

        # Currently bulk-save is broken in django-rest-framework so we have
        # to implement ourselves. See:
        # https://github.com/tomchristie/django-rest-framework/issues/1965
        # TODO: potentially subclass serializers.ListSerializer with child
        # SurgeLevelSerializer

        for i, record in enumerate(request.data):
            serializer = SurgeLevelSerializer(
                data=record, context=context)

            if serializer.is_valid():
                serializer.save(location=location)
            else:
                error_dict = {
                    'detail': 'Failed to deserialize item [{}].'.format(i)}
                error_dict.update(serializer.errors)
                raise InvalidDataError(error_dict)

        return Response({'detail': 'OK.'}, status=status.HTTP_200_OK)

    def get_serializer(self, instance=None, data=None):
        assert instance is None and data is None, (
            'instance={}, data={}'.format(instance, data))
        return SurgeLevelSerializer()

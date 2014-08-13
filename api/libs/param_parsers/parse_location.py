from django.core.exceptions import ObjectDoesNotExist

from api.apps.locations.models import Location

from .exceptions import InvalidLocationError


def parse_location(location_slug):
    """
    From a location slug ie 'liverpool-gladstone-dock', return a Location model
    object or blow up with an appropriate API Exception.
    """
    if location_slug is None:
        raise InvalidLocationError(
            'No location given, see locations endpoint.')

    try:
        location = Location.objects.get(slug=location_slug)
    except ObjectDoesNotExist:
        raise InvalidLocationError(
            'Invalid location: "{}". See locations endpoint.'.format(
                location_slug))
    return location

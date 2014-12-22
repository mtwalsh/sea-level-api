from django.test import TestCase
from nose.tools import assert_equal

from api.apps.locations.models import Location


class TestLocation(TestCase):
    def test_that_visible_defaults_to_true(self):
        location = Location.objects.create(slug='foo', name='Foo')
        assert_equal(True, location.visible)

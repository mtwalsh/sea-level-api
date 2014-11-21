from nose.tools import assert_equal
from django.test import TestCase

from api.apps.tide_gauges.models import TideGauge, TideGaugeLocationLink
from api.apps.locations.models import Location


class TestLinkedLocation(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.gauge_unlinked = TideGauge.objects.create(slug='unlinked')
        cls.gauge_linked = TideGauge.objects.create(slug='linked')
        cls.linked_location = Location.objects.create(slug='somelocation')
        cls.link = TideGaugeLocationLink.objects.create(
            tide_gauge=cls.gauge_linked,
            location=cls.linked_location)

    @classmethod
    def tearDownClass(cls):
        cls.gauge_unlinked.delete()
        cls.gauge_linked.delete()
        cls.linked_location.delete()
        cls.link.delete()

    def test_that_linked_location_returns_none_for_unlinked_gauge(self):
        assert_equal(None, self.gauge_unlinked.linked_location)

    def test_that_linked_location_returns_location_for_linked_gauge(self):
        assert_equal(self.linked_location, self.gauge_linked.linked_location)

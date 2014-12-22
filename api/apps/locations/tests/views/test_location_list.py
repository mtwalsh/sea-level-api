from django.test import TestCase

from nose.tools import assert_equal, assert_in

from api.apps.locations.models import Location
from api.libs.test_utils import decode_json


class TestLocationList(TestCase):
    PATH = '/1/locations/'

    @classmethod
    def setUpClass(cls):
        cls.liverpool = Location.objects.create(
            slug='liverpool', name='Liverpool')

        cls.southampton = Location.objects.create(
            slug='southampton', name='Southampton')

    @classmethod
    def tearDownClass(cls):
        Location.objects.all().delete()

    def test_that_locations_endpoint_returns_http_200(self):
        self.response = self.client.get(self.PATH)
        assert_equal(200, self.response.status_code)

    def test_that_locations_endpoint_json_has_locations_field(self):
        self.response = self.client.get(self.PATH)
        assert_in('locations', decode_json(self.response.content))

    def test_that_each_location_has_correct_fields(self):
        expected_fields = set(['name', 'slug', 'url'])

        self.response = self.client.get(self.PATH)
        for location in decode_json(self.response.content)['locations']:
            assert_equal(expected_fields, set(location.keys()))

    def test_that_locations_are_serialized_correctly(self):
        self.response = self.client.get(self.PATH)
        expected = [
            {
                'name': 'Liverpool',
                'slug': 'liverpool',
                'url': 'http://testserver/1/locations/liverpool/',
            },
            {
                'name': 'Southampton',
                'slug': 'southampton',
                'url': 'http://testserver/1/locations/southampton/'
            }]
        assert_equal(expected, decode_json(self.response.content)['locations'])

    def test_that_non_visible_locations_arent_listed(self):
        hidden_location = Location.objects.create(
            slug='hidden', name='Hidden', visible=False)
        self.response = self.client.get(self.PATH)

        endpoint_slugs = set([l['slug'] for l in decode_json(
            self.response.content)['locations']])

        assert_equal(set(['southampton', 'liverpool']), endpoint_slugs)

        hidden_location.delete()

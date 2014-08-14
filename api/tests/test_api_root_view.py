from django.test import TestCase
from nose.tools import assert_equal, assert_in

from api.libs.test_utils import decode_json


class TestAPIRootView(TestCase):
    fixtures = [
        'api/apps/locations/fixtures/two_locations.json',
        'api/apps/predictions/fixtures/predictions_two_locations.json',
    ]

    @staticmethod
    def expand_path(path):
        return 'http://testserver' + path

    def test_that_root_url_with_no_version_redirects_to_v1(self):
        response = self.client.get('/')
        assert_equal(302, response.status_code)
        assert_equal(self.expand_path('/1/'), response['Location'])

    def test_that_envelope_has_links_field(self):
        response = self.client.get('/1/')
        data = decode_json(response.content)
        assert_in('links', data)

    def test_that_root_api_has_correct_links(self):
        response = self.client.get('/1/')
        data = decode_json(response.content)

        expected_paths = [
            '/1/locations/',
            '/1/predictions/tide-levels/',
            '/1/predictions/tide-windows/',
            '/1/sea-levels/',
        ]

        assert_equal(
            set([self.expand_path(p) for p in expected_paths]),
            set([link['href'] for link in data['links']])
        )

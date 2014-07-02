from django.test import TestCase
from nose.tools import assert_equal, assert_in, assert_not_in


class TestCORSHeaders(TestCase):
    fixtures = [
        'api/apps/locations/fixtures/two_locations.json',
    ]

    def setUp(self):
        self.resp = self.send_preflight_request()

    def send_preflight_request(self):
        return self.client.options(
            '/1/',
            HTTP_HOST='api.sealevelresearch.com',
            HTTP_ORIGIN='http://www.sealevelresearch.com',
            HTTP_ACCESS_CONTROL_REQUEST_METHOD='GET',
            HTTP_ACCESS_CONTROL_REQUEST_HEADERS='Content-Type')

    def test_that_api_sets_allow_origin_header(self):
        assert_in('Access-Control-Allow-Origin', self.resp)

    def test_that_api_allows_all_cors_origins(self):
        assert_equal('*', self.resp['Access-Control-Allow-Origin'])

    def test_that_api_allows_only_get_method(self):
        assert_equal('GET, OPTIONS', self.resp['Access-Control-Allow-Methods'])

    def test_that_api_allows_content_type_header(self):
        expected_headers = [
            'x-requested-with',
            'content-type',
            'accept',
            'origin',
            'authorization',
            'x-csrftoken',
        ]
        assert_equal(
            ', '.join(expected_headers),
            self.resp['Access-Control-Allow-Headers'])

    def test_that_api_disallows_cors_credentials(self):
        # Don't include cookies - we don't want credentials leaked to us.
        # Strangely, servers should omit rather than set to false.
        assert_not_in('Access-Control-Allow-Credentials', self.resp)

    def test_that_api_preflight_response_advertises_one_hour_cache(self):
        expected_age = '{}'.format(3 * 3600)  # 3 hours
        assert_equal(expected_age, self.resp['Access-Control-Max-Age'])

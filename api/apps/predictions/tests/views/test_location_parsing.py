from nose.tools import assert_equal

from api.libs.test_utils import decode_json


class LocationParsingTestMixin(object):

    def test_that_no_location_gives_link_to_locations_endpoint(self):
        response = self.client.get(self.BASE_PATH)
        assert_equal(404, response.status_code)
        data = decode_json(response.content)
        assert_equal(
            {'detail': 'No location given, see locations endpoint.'},
            data
        )

    def test_that_invalid_location_gives_a_json_404(self):
        response = self.client.get(self.BASE_PATH + 'invalid/')
        assert_equal(404, response.status_code)
        data = decode_json(response.content)
        assert_equal(
            {'detail': 'Invalid location: "invalid". See locations endpoint.'},
            data
        )

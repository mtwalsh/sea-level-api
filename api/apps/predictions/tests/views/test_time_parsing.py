from nose.tools import assert_equal

from api.libs.test_utils import decode_json


class TimeParsingTestMixin(object):

    def test_that_no_start_parameter_is_an_error(self):
        response = self.client.get(
            self.BASE_PATH + 'liverpool/?end=2014-01-01T00:00:00Z')
        assert_equal(400, response.status_code)
        assert_equal(
            'Missing parameter `start`. Format: 2014-11-30T00:00:00Z',
            decode_json(response.content)['detail'])

    def test_that_no_end_parameter_is_an_error(self):
        response = self.client.get(
            self.BASE_PATH + 'liverpool/?start=2014-01-01T00:00:00Z')
        assert_equal(400, response.status_code)
        assert_equal(
            'Missing parameter `end`. Format: 2014-11-30T00:00:00Z',
            decode_json(response.content)['detail'])

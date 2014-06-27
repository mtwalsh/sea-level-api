from nose.tools import assert_equal
from nose.plugins.skip import SkipTest


class TimeParsingTestMixin(object):

    def test_that_no_start_and_end_parameter_temporary_redirects_to_now(self):
        raise SkipTest("Not yet implemented.")
        response = self.client.get(self.PATH + 'liverpool/')
        assert_equal(302, response.status_code)

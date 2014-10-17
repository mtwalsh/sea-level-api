import json

from nose.tools import assert_equal

from django.conf import settings
from django.contrib.auth.models import Permission, User

from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from api.apps.locations.models import Location
from api.apps.predictions.models import SurgePrediction
from api.libs.test_utils import decode_json

_URL = '/1/predictions/surge-levels/liverpool/'


def make_users():
    permitted = User.objects.create_user('permitted', '', 'password')
    Token.objects.create(user=permitted)

    forbidden = User.objects.create_user('forbidden', '', 'password')
    Token.objects.create(user=forbidden)
    permitted.user_permissions.add(
        Permission.objects.get(codename='add_surgeprediction'))

    return permitted, forbidden


def delete_users():
    User.objects.get(username='permitted').delete()
    User.objects.get(username='forbidden').delete()


class PostJsonMixin(object):
    def _post_json(self, data, **extras):
        return self.client.post(_URL,
                                data=json.dumps(data),
                                content_type='application/json',
                                **extras)


class TestSurgeLevelsEndpoint(APITestCase, PostJsonMixin):
    @classmethod
    def setUpClass(cls):
        cls.liverpool = Location.objects.create(
            slug='liverpool', name='Liverpool')

        cls.PREDICTION_A = {
            "datetime": "2014-06-10T10:34:00Z",
            "surge_level": 0.23
        }

        cls.PREDICTION_B = {
            "datetime": "2014-06-10T10:34:00Z",  # same as A
            "surge_level": -0.15
        }

        cls.PREDICTION_C = {
            "datetime": "2014-06-10T11:00:00Z",
            "surge_level": 0.50
        }
        (cls.user, _) = make_users()

    @classmethod
    def tearDownClass(cls):
        cls.liverpool.delete()
        delete_users()

    def setUp(self):
        self.client.force_authenticate(user=self.user)
        SurgePrediction.objects.all().delete()

    @staticmethod
    def _serialize(prediction):
        return {
            'datetime': prediction.minute.datetime.strftime(
                settings.DATETIME_FORMAT),
            'surge_level': prediction.surge_level
        }

    def test_that_http_options_allowed_methods_are_post_and_options(self):
        response = self.client.options(_URL)
        assert_equal(200, response.status_code)
        assert_equal('POST, OPTIONS', response['Allow'])

    def test_that_http_get_is_not_allowed(self):
        response = self.client.get(_URL)
        assert_equal(405, response.status_code)
        assert_equal(
            {'detail': "Method 'GET' not allowed."},
            decode_json(response.content))

    def test_that_valid_http_post_returns_json_message(self):
        response = self._post_json([self.PREDICTION_A])
        assert_equal({"detail": "OK."}, decode_json(response.content))

    def test_that_valid_http_post_returns_http_200(self):
        response = self._post_json([self.PREDICTION_A])
        assert_equal(200, response.status_code)

    def test_that_passing_a_non_list_json_object_gives_sane_error(self):
        response = self._post_json(self.PREDICTION_A)

        assert_equal(400, response.status_code)
        assert_equal({'detail': 'Data must be inside a JSON array eg []'},
                     decode_json(response.content))

    def test_that_http_post_can_create_single_surge_prediction(self):
        response = self._post_json([self.PREDICTION_A])
        assert_equal(200, response.status_code)

        assert_equal(1, SurgePrediction.objects.all().count())
        assert_equal(self.PREDICTION_A,
                     self._serialize(SurgePrediction.objects.all()[0]))

    def test_that_http_post_can_create_multiple_surge_predictions(self):
        response = self._post_json([self.PREDICTION_A, self.PREDICTION_C])

        assert_equal(200, response.status_code)
        assert_equal(2, SurgePrediction.objects.all().count())

        ob_1, ob_2 = SurgePrediction.objects.all()
        assert_equal(self.PREDICTION_A, self._serialize(ob_1))
        assert_equal(self.PREDICTION_C, self._serialize(ob_2))

    def test_that_http_post_can_overwrite_surge_prediction(self):
        response = self._post_json([self.PREDICTION_A])
        assert_equal(200, response.status_code)
        response = self._post_json([self.PREDICTION_B])
        assert_equal(200, response.status_code)

        assert_equal(1, SurgePrediction.objects.all().count())
        assert_equal(self.PREDICTION_B,
                     self._serialize(SurgePrediction.objects.all()[0]))

    def test_that_one_bad_record_causes_all_records_to_fail(self):
        bad = {'datetime': 'invalid', 'surge_level': 0.23}
        response = self._post_json(
            [self.PREDICTION_A, bad])
        assert_equal(400, response.status_code)
        assert_equal(0, SurgePrediction.objects.all().count())

    def test_that_datetime_without_timezone_is_rejected(self):
        doc = {
            "datetime": "2014-06-10T10:34:00",
            "surge_level": 0.23
        }
        response = self._post_json([doc])
        assert_equal(400, response.status_code)
        assert_equal(
            {
                'detail': 'Failed to deserialize item [0].',
                'datetime': ['Datetime has wrong format. Use one of these '
                             'formats instead: YYYY-MM-DDThh:mm:00Z']
            },
            decode_json(response.content))

    def test_that_datetime_with_non_utc_timezone_is_rejected(self):
        doc = {
            "datetime": "2014-06-10T10:34:00+02:00",
            "surge_level": 0.23
        }
        response = self._post_json([doc])
        assert_equal(400, response.status_code)
        assert_equal(
            {
                'detail': 'Failed to deserialize item [0].',
                'datetime': ['Datetime has wrong format. Use one of these '
                             'formats instead: YYYY-MM-DDThh:mm:00Z']
            },
            decode_json(response.content))

    def test_that_datetime_with_seconds_is_rejected(self):
        doc = {
            "datetime": "2014-06-10T10:34:45Z",
            "surge_level": 0.23
        }
        response = self._post_json([doc])
        assert_equal(400, response.status_code)
        assert_equal(
            {
                'detail': 'Failed to deserialize item [0].',
                'datetime': ['Datetime has wrong format. Use one of these '
                             'formats instead: YYYY-MM-DDThh:mm:00Z']
            },
            decode_json(response.content))


class TestSurgeLevelsEndpointAuthentication(APITestCase, PostJsonMixin):
    @classmethod
    def setUpClass(cls):
        cls.liverpool = Location.objects.create(
            slug='liverpool', name='Liverpool')
        (cls.permitted, cls.forbidden) = make_users()
        cls.good_data = {
            "datetime": "2014-06-10T10:34:00Z",
            "surge_level": 0.23
        }

    @classmethod
    def tearDownClass(cls):
        cls.liverpool.delete()
        delete_users()

    def test_that_no_authentication_header_returns_http_401(self):
        # 401 vs 403: http://stackoverflow.com/a/6937030
        response = self._post_json([])
        assert_equal(401, response.status_code)

    def test_that_user_without__add_surgeprediction__permission_gets_403(self):
        token = Token.objects.get(user__username='forbidden').key
        response = self._post_json(
            [self.good_data], HTTP_AUTHORIZATION='Token {}'.format(token))
        assert_equal(403, response.status_code)
        assert_equal(
            {'detail': 'You do not have permission to perform this action.'},
            decode_json(response.content))

    def test_that_user_with__add_surgeprediction__permission_can_post(self):
        token = Token.objects.get(user__username='permitted').key
        response = self._post_json(
            [self.good_data], HTTP_AUTHORIZATION='Token {}'.format(token))
        assert_equal(200, response.status_code)

from rest_framework.exceptions import APIException


class MissingParameterException(APIException):
    status_code = 400
    default_detail = 'Missing query parameter in URL.'


class InvalidLocationError(APIException):
    status_code = 404
    default_detail = 'Invalid location specified. See the locations endpoint.'

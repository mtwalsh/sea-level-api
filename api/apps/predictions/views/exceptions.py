from rest_framework.exceptions import APIException


class MissingParameterException(APIException):
    status_code = 400
    default_detail = 'Missing query parameter in URL.'


class InvalidParameterError(APIException):
    status_code = 400
    default_detail = 'Invalid value for query parameter'


class NoStartTimeGivenError(MissingParameterException):
    default_detail = 'Missing parameter `start`. Format: 2014-11-30T00:00:00Z'


class NoEndTimeGivenError(MissingParameterException):
    default_detail = 'Missing parameter `end`. Format: 2014-11-30T00:00:00Z'


class InvalidLocationError(APIException):
    status_code = 404
    default_detail = 'Invalid location specified. See the locations endpoint.'

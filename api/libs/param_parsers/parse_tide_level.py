from .exceptions import MissingParameterError, InvalidParameterError


def parse_tide_level(tide_level_param):
    if tide_level_param is None:
        raise MissingParameterError(
            'Missing required query parameter `tide_level`')
    try:
        return float(tide_level_param)
    except ValueError:
        raise InvalidParameterError(
            'Invalid floating point value for `tide_level`: "{}"'.format(
                tide_level_param))

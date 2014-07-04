import json


def decode_json(response_json):
    return json.loads(response_json.decode('utf-8'))

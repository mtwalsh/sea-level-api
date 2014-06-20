from rest_framework.renderers import JSONRenderer

from .json_envelope_renderer import JSONEnvelopeRenderer


def replace_json_renderer(renderer_classes):
    """
    Return a list of renderers where the stock JSONRenderer is replaced with
    the JSONEnvelopeRenderer.
    """
    new_renderers = list(renderer_classes)

    index = new_renderers.index(JSONRenderer)
    new_renderers[index] = JSONEnvelopeRenderer

    return new_renderers

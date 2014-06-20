from rest_framework import renderers


class JSONEnvelopeRenderer(renderers.JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):

        data = JSONEnvelopeRenderer.wrap_data(data, renderer_context)

        return super(JSONEnvelopeRenderer, self) \
            .render(data, accepted_media_type, renderer_context)

    @staticmethod
    def wrap_data(data, renderer_context):

        if not hasattr(renderer_context.get('view'), 'get_serializer'):
            return data
        else:
            resource_name = getattr(
                renderer_context.get('view').get_serializer().Meta,
                'resource_name',
                'items')
            return {resource_name: data}

    @staticmethod
    def wrap_data_more(data, renderer_context):
        json_envelope = getattr(
            renderer_context.get('view').get_serializer().Meta,
            'json_envelope',
            {})

        resource_name = json_envelope.get('resource_name', 'items')
        meta = json_envelope.get('meta', None)
        links = json_envelope.get('links', None)
        linked = json_envelope.get('links', None)

        data = {
            resource_name: data,
            'meta': meta,
            'links': links,
            'linked': linked
        }

        return {k: v for k, v in data.iteritems() if v is not None}

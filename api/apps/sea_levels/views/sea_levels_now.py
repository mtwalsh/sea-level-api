import datetime

from api.libs.view_helpers import format_datetime, now_rounded

from .sea_levels import SeaLevels


class SeaLevelsNow(SeaLevels):
    """
    Get Sea Levels for the next twenty-four hours. This is a convenience
    endpoint so that you don't have to explicitly set `start` and `end`
    """

    def get_queryset(self, *args, **kwargs):
        new_query_params = self.request.query_params.copy()  # make mutable

        now = now_rounded()
        now_plus_24 = now + datetime.timedelta(hours=24)

        new_query_params.update({
            'start': format_datetime(now),
            'end': format_datetime(now_plus_24),
        })

        return super(SeaLevelsNow, self).get_queryset(
            query_params=new_query_params, *args, **kwargs)

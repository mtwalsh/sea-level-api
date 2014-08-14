# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


CREATE_VIEW = """
CREATE VIEW sea_levels_combinedpredictionobservation AS
    SELECT minute_in_time_minute.datetime AS datetime,
           predictions_prediction.location_id       AS location_id,
           predictions_prediction.tide_level        AS predicted_tide_level,
           observations_observation.sea_level       AS observed_sea_level,
           (observations_observation.sea_level
            - predictions_prediction.tide_level)    AS derived_surge_level
    FROM predictions_prediction
    LEFT OUTER JOIN minute_in_time_minute
        ON predictions_prediction.minute_id = minute_in_time_minute.id
    LEFT OUTER JOIN observations_observation
        ON minute_in_time_minute.id = observations_observation.minute_id
        AND predictions_prediction.location_id
            = observations_observation.location_id;
"""

DELETE_VIEW = """
DROP VIEW IF EXISTS sea_levels_combinedpredictionobservation;
"""


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.RunSQL(
            sql=CREATE_VIEW,
            reverse_sql=DELETE_VIEW),
    ]

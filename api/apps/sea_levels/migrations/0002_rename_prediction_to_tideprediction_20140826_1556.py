# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


CREATE_VIEW = """
DROP VIEW IF EXISTS sea_levels_combinedpredictionobservation;
CREATE VIEW sea_levels_combinedpredictionobservation   AS
    SELECT minute_in_time_minute.datetime AS datetime,
           predictions_tideprediction.location_id     AS location_id,
           predictions_tideprediction.tide_level      AS predicted_tide_level,
           observations_observation.sea_level          AS observed_sea_level,
           (observations_observation.sea_level
            - predictions_tideprediction.tide_level)   AS derived_surge_level
    FROM predictions_tideprediction
    LEFT OUTER JOIN minute_in_time_minute
        ON predictions_tideprediction.minute_id = minute_in_time_minute.id
    LEFT OUTER JOIN observations_observation
        ON minute_in_time_minute.id = observations_observation.minute_id
        AND predictions_tideprediction.location_id
            = observations_observation.location_id;
"""


class Migration(migrations.Migration):

    dependencies = [
        ('sea_levels', '0001_initial'),
    ]

    operations = [
        migrations.RunSQL(
            sql=CREATE_VIEW),
    ]

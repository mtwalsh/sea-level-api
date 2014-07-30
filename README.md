[![Build Status](https://travis-ci.org/sealevelresearch/sea-level-api.svg?branch=master)](https://travis-ci.org/sealevelresearch/sea-level-api)

# Sea Level API v1

** Warning: This is an alpha API and may change dramatically - don't develop against it without
contacting us first! **

| Type of Endpoint           | Data class  | Source      | URL base
| -------------------------- | ----------- | ----------- | ----------------------------
| point-in-time predictions  | tide level  | astro model | **/predictions/tide-levels/**
|                            | surge level | hydro model | /predictions/surge-levels/
|                            | sea level   | *derived*   | /predictions/sea-levels/
| point-in-time observations | sea level   | tide gauge  | /observations/sea-levels/
|                            | surge level | *derived*   | /observations/surge-levels/
| combined prediction/obs    | sea level   | *derived*   | /sea-levels/
| time window predictions    | tide level  | *derived*   | **/predictions/tide-windows/**
|                            | sea level   | *derived*   | /predictions/sea-level-windows/


## Datetime and "now"

- All datetimes are expressed in UTC
- Datetimes are always formatted as `YYYY-MM-DDThh:mm:ssZ` (a subset of ISO 8601)


## /predictions/tide-levels/

- `start` and `end` - date/times between which tide levels are returned.
- `interval` - number of minutes between results (default=1)


[/predictions/tide-levels/liverpool-gladstone-dock/?start=2014-06-03T15:47:00Z&end=2014-06-03T15:48:00Z](http://api.sealevelresearch.com/1/predictions/tide-levels/liverpool-gladstone-dock/?start=2014-06-03T15:47:00Z&end=2014-06-03T15:48:00Z)

```json
{
  "tide_levels": [{
    "datetime": "2014-06-03T15:47:00Z",
    "tide_level": 10.37,
  }],
}
```

[/predictions/tide-levels/liverpool-gladstone-dock/now/](http://api.sealevelresearch.com/1/predictions/tide-levels/liverpool-gladstone-dock/now/)

## /predictions/tide-windows/

- `start` and `end` - date/time bounds inside which to search for tidal windows.
- `tide_level` - the minimum tide height in metres.

Returns time windows during which the tide level will be above a given height in metres.

[/predictions/tide-windows/liverpool-gladstone-dock?start=2014-06-01T18:00:00Z&end=2014-06-02T18:00:00Z&tide_level=10.7](http://api.sealevelresearch.com/1/predictions/tide-windows/liverpool-gladstone-dock?start=2014-06-01T18:00:00Z&end=2014-06-02T18:00:00Z&tide_level=10.7)
```json

{
  "tide_windows": [{
    "start": {
      "datetime": "2014-06-03T18:00:00Z",
      "tide_level": 10.71
      },
    "end": {
      "datetime": "2014-06-03T19:21:00Z",
      "tide_level": 10.73
      },
    "duration": {
      "total_seconds": 4860,
    },
  }],
}
```

[/predictions/tide-windows/liverpool-gladstone-dock/now/?tide_level=10.7](http://api.sealevelresearch.com/1/predictions/tide-windows/liverpool-gladstone-dock/now/?tide_level=10.7)


## /predictions/sea-levels/ (draft)

```
{
  "sea_levels": [
    "datetime": "2014-08-01T16:14:00Z",
    "sea_level": 8.85,
    "tide_level": 8.45,
    "surge_level": 0.20,
  ]
}
```

## /sea-levels/ (draft)

```
{
  "sea_levels": [
  {
    "datetime": "2014-08-01T16:14:00Z",
    "predicted_tide_level": 8.45,
    "predicted_surge_level": 0.20,
    "predicted_sea_level": 8.65,
    "observed_sea_level": 8.70,
    "derived_surge_level": 0.25,
  }
  ]
}
```

## Design notes

- http://jsonapi.org/format/
- http://blog.2partsmagic.com/restful-uri-design/


# Deploying a Heroku app

After setting up a new app, you need to configure a number of environment
variables through the herkou command line, for example:

```
APP_NAME="sea-level-api-staging"
DOMAIN="api-staging.sealevelresearch.com"

# DJANGO_SETTINGS_MODULE
heroku config:set DJANGO_SETTINGS_MODULE=api.settings.production --app ${APP_NAME}

# DATABASE
heroku addons:add heroku-postgresql:dev --app ${APP_NAME}
heroku pg:promote <name of database ie HEROKU_POSTGRESQL_ROSE_URL> --app ${APP_NAME}
heroku addons:add pgbackups --app ${APP_NAME}

# SECRET_KEY
heroku config:set SECRET_KEY=$(openssl rand -base64 64) --app ${APP_NAME}

# DOMAINS
heroku domains:add ${DOMAIN} --app ${APP_NAME}

# WORKERS (after first deploy)
heroku ps:scale web=1 --app ${APP_NAME}
```


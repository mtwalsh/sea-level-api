[![Build Status](https://travis-ci.org/sealevelresearch/sea-level-api.svg?branch=master)](https://travis-ci.org/sealevelresearch/sea-level-api)

# Documentation

Lives at [http://sealevelresearch.github.io/sea-level-api/](http://sealevelresearch.github.io/sea-level-api/)

# Configuring a new Heroku app

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

# API design notes

See:

- http://jsonapi.org/format/
- http://blog.2partsmagic.com/restful-uri-design/


## Business objects

- TidePrediction
  - datetime
  - height

- SurgePrediction
  - datetime
  - height

- SeaLevelPrediction
  - tide level prediction
  - surge level prediction
  - eg 8.7m tide + 0.3m surge

- SeaLevelTimeWindow
  - datetime of start
  - datetime of end


## Low-level objects

- Height
  - water level in metres

- Datetime
  - date & time, *always* presented in UTC
  - represented in ISO 8601 format subset

- Location
  - latitude & longitude
  - timezone name eg "Europe/London"
  - note: *may* have a tide gauge


## Datetimes & timezones

- All datetimes are expressed in UTC.
- Communication into and out of the API will be done in terms of UTC.

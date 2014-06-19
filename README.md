[![Build Status](https://travis-ci.org/sealevelresearch/sea-level-api.svg)](https://travis-ci.org/sealevelresearch/sea-level-api)

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


## Datetime and "now"

- All datetimes are expressed in UTC
- Datetimes are always formatted as `YYYY-MM-DDThh:mm:ssZ` (a subset of ISO 8601)



## Tide Prediction

### Get one tide prediction for 2014-06-03 15:47:00 at Liverpool Gladstone

`/v0.1/predictions/liverpool-gladstone/2014-06-03T15:47:00Z`

```json
{
  "predictions": [{
    "datetime": "2014-06-03T15:47:00Z",
    "sea_level_height": {
      "value":  10.90,
      "unit": "metres",
    },
    "tide_height": {
      "value":  10.37,
      "unit": "metres",
    },
    "surge_height": {
      "value":  0.53,
      "unit": "metres",
    },
  }],
  "linked": {
    "locations": [{
      "id": "liverpool-gladstone",
      "timezone": "Europe/London",
      "name": "Gladstone Dock, Liverpool",
      "latitude": 53.00,
      "longitude": -3.00
    }]
  },
}
```

### Get an hourly range of tide predictions

`/v0.1/predictions/liverpool-gladstone?start=2014-06-03T15:47:00Z&end=2014-06-03T16:47:00Z`

### Get the current tide prediction at Liverpool Gladstone (redirect)

`/v0.1/predictions/liverpool-gladstone/now` ==> eg `/v0.1/predictions/liverpool-gladstone/2014-06-03T15:47:00Z`

### Get the next hour of tide predictions at Liverpool Gladstone (redirect)

`/v0.1/predictions/liverpool-gladstone` ==> eg `/v0.1/predictions/liverpool-gladstone?start=2014-06-03T15:47:00Z&end=2014-06-03T16:47:00Z`


## Sea Level Time Window

### Get time windows between 2014-06-01 and 2014-06-02 where the height will be above 10.7 metres

`/v0.1/time-windows/liverpool-gladstone?start=2014-06-01T18:00:00Z&end=2014-06-02T18:00:00Z&height=10.7`

```json

{
  "time_windows": [{
    "start": {
      "datetime": "2014-06-03T18:00:00Z",
      },
    "end": {
      "datetime": "2014-06-03T19:21:00Z",
      },
    "duration": {
      "total_seconds": 4860,
    },
  }],
  "linked": {
    "locations": [{
      "id": "liverpool-gladstone",
      "timezone": "Europe/London",
      "name": "Gladstone Dock, Liverpool",
      "latitude": 53.00,
      "longitude": -3.00
    }]
  }
}
```

### Get the next time window where the height will be above 10.7 metres (redirect)

`/v0.1/time-windows/liverpool-gladstone/next?height=10.7` => `/v0.1/time-windows/liverpool-gladstone?start=2014-06-01T18:00:00Z&end=2014-06-02T18:00:00Z&height=10.7`

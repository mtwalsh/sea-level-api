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



## Tide Level Prediction

### Get a single tide predictions for 2014-06-03 15:47:00 UTC at Liverpool Gladstone

`/predictions/tide-levels/liverpool-gladstone/?start=2014-06-03T15:47:00Z&end=2014-06-03T15:48:00Z`

```json
{
  "tide_levels": [{
    "datetime": "2014-06-03T15:47:00Z",
    "tide_level": 10.37,
  }],
}
```

## Tide Time Window [in progress]

### Get time windows between 2014-06-01 and 2014-06-02 where the height will be above 10.7 metres

`/predictions/tide-time-windows/liverpool-gladstone?start=2014-06-01T18:00:00Z&end=2014-06-02T18:00:00Z&height=10.7`

```json

{
  "tide-time_windows": [{
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

`/time-windows/liverpool-gladstone/next?height=10.7` => `/time-windows/liverpool-gladstone?start=2014-06-01T18:00:00Z&end=2014-06-02T18:00:00Z&height=10.7`

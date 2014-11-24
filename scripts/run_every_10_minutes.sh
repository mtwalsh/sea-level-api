#!/bin/bash -x

function download_ea_measurements {
  python manage.py get_latest_ea_measurements
}

function convert_ea_measurements_into_observations {
  python manage.py convert_measurements
}

pushd $(dirname $0)/..

download_ea_measurements
# convert_ea_measurements_into_observations

popd

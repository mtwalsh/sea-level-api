#!/bin/bash -x

function download_ea_measurements {
  python manage.py get_latest_ea_measurements
}

pushd $(dirname $0)/..

download_ea_measurements

popd

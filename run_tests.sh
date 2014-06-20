#!/bin/bash -e

function run_pep8_style_checks {
    # F401: imported but unused
    flake8 \
        --ignore=F401 \
        --exclude='api/apps/*/migrations/*.py,api/settings/*.py' \
    .
}


function run_python_unit_tests {
    python manage.py test
}

run_pep8_style_checks
run_python_unit_tests

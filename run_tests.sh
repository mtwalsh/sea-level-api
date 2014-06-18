#!/bin/bash -e

function run_pep8_style_checks {
    flake8 .
}


function run_python_unit_tests {
    python manage.py test
}

run_python_unit_tests
run_pep8_style_checks  # TODO: reorder once PEP8 tests are OK

#!/bin/sh

set -e

readonly INTEGRATION_TESTS_TARGET="${1}" # set in Makefile. Defaults to integration_tests

pytest -vv --capture=no --cov=. --cov-config=.coveragerc \
       -o junit_family=xunit1 --junitxml=htmlcov/junit.xml \
       -W ignore::pytest.PytestCollectionWarning \
         "${INTEGRATION_TESTS_TARGET}"

# Generate html results
coverage html

# Add json stats to htmlcov folder
coverage json -o htmlcov/coverage.json

# Add report
coverage report -m > htmlcov/summary.txt

# Create a file containing the coverage percentage
coverage report | grep TOTAL | awk '{print "COVERAGE=\""$4"\""}' > htmlcov/test_coverage.txt

# Create a file containing the number of test cases
TEST_CASES=`pytest --collect-only -q  --ignore=integration_tests | head -n -2 | wc -l`
echo TEST_CASES=$TEST_CASES > htmlcov/test_cases.txt

#!/bin/sh

set -e

# ${1} is set in Makefile.
# Defaults to integration_tests/ (the dir name)
# To run an individual test file...
# $ make test_integration TARGET=test_approvals.py
# which will result in ${1}==integration_tests/test_approvals.py
readonly TARGET="${1}"

pytest -vv --capture=no --cov=. --cov-config=.coveragerc \
       -o junit_family=xunit1 --junitxml=htmlcov/junit.xml \
       -W ignore::pytest.PytestCollectionWarning \
       --approvaltests-use-reporter='PythonNative' \
         "${TARGET}"

# Generate html results
coverage html

# Add json stats to htmlcov folder
coverage json -o htmlcov/coverage.json

# Add report
readonly REPORT_FILENAME=htmlcov/summary.txt
coverage report -m > "${REPORT_FILENAME}"

# Create a file containing the coverage percentage
cat "${REPORT_FILENAME}" | grep TOTAL | awk '{print "COVERAGE=\""$4"\""}' > htmlcov/test_coverage.txt

# Create a file containing the number of test cases
TEST_CASES=`pytest --collect-only -q  --ignore=integration_tests | head -n -2 | wc -l`
echo TEST_CASES=$TEST_CASES > htmlcov/test_cases.txt

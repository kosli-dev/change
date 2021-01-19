#!/bin/sh

set -e

# ${1} is set in the Makefile.
# Defaults to tests/ (the dir name)
# To run an individual test file...
# $ make test TARGET=test_create_release.py
# which will result in ${1}==tests/test_release.py
readonly TARGET="${1}"

# Beware using --approvaltests-use-reporter='PythonNative'
# See comment in tests/utils/verify_approval.py

pytest \
       --capture=no \
       --cov=. \
       --junitxml=htmlcov/junit.xml \
       -o junit_family=xunit1 \
       --verbose \
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

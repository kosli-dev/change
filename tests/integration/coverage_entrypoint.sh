#!/bin/sh

set -eu

# ${1} is set in the Makefile.
# Defaults to tests/integration/ (the dir name)
# To run an individual test file...
# $ make test_integration TARGET=test_NAME.py
# which will result in ${1}==tests/integration/test_NAME.py
readonly TARGET="${1}"

# Beware using --approvaltests-use-reporter='PythonNative'
# See comment in tests/unit/utils/verify_approval.py

# pytest-cov command line options are documented here
# https://pytest-cov.readthedocs.io/en/latest/config.html

pytest \
       --random-order-bucket=global \
       --capture=no \
       --cov=source/ \
       --junitxml=htmlcov/junit.xml \
       -o junit_family=xunit1 \
       --verbose \
         "${TARGET}"

# coverage is documented here
# https://coverage.readthedocs.io/en/v4.5.x/index.html

# Generate html results
coverage html

# Add json stats to htmlcov folder
coverage json -o htmlcov/coverage.json

# Add report
readonly REPORT_FILENAME=htmlcov/summary.txt
coverage report -m > "${REPORT_FILENAME}"

# Create a file containing the coverage percentage
cat "${REPORT_FILENAME}" | grep TOTAL | awk '{print "COVERAGE=\""$4"\""}' > htmlcov/test_coverage.sh

# Create a file containing the number of test cases
TEST_CASES=`pytest --collect-only -q  --ignore=tests/integration | head -n -2 | wc -l`
echo TEST_CASES=$TEST_CASES > htmlcov/test_cases.sh

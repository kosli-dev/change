#!/bin/sh

set -eu

# TARGET
# ${1} is set in the Makefile.
# Defaults to tests/unit/ (the dir name)
# which runs all the tests

readonly TARGET="${@:-tests/unit/}"

# pytest-cov command line options are documented here
# https://pytest-cov.readthedocs.io/en/latest/config.html

mkdir /data || true  # for Merkelypipe.json to be copied into

pytest \
       --random-order-bucket=global \
       --capture=no \
       --cov-config=tests/unit/.coveragerc \
       --cov=source/ \
       --cov=tests/ \
       --cov-branch \
       --junitxml=htmlcov/junit.xml \
       -o junit_family=xunit1 \
       --pythonwarnings=ignore::pytest.PytestCollectionWarning \
       --verbose \
         ${TARGET}

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
cat "${REPORT_FILENAME}" | grep TOTAL | awk '{print "TEST_BRANCH_COVERAGE=\""$6"\""}' | sed 's/%//g' > htmlcov/test_branch_coverage.sh

# Create a file containing the number of test cases
TEST_CASE_COUNT=`pytest --collect-only -q | head -n -2 | wc -l`
echo TEST_CASE_COUNT=${TEST_CASE_COUNT} > htmlcov/test_case_count.sh

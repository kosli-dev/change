#!/bin/sh

set -eu

# TARGET
# ${1} is set in the Makefile.
# Defaults to tests/unit/ (the dir name)
# which runs all the tests

# To run a single test file...
# $ make test_unit TARGET=FILENAME
# which will result in ${1}==tests/unit/FILENAME

# To run a single test...
# $ make test_unit TARGET=FILENAME::TESTNAME
# which will result in ${1}==tests/unit/FILENAME::TESTNAME

readonly TARGET="${1}"

# pytest-cov command line options are documented here
# https://pytest-cov.readthedocs.io/en/latest/config.html

mkdir /data || true  # for Merkelypipe.json to be copied into

pytest \
       --random-order-bucket=global \
       --capture=no \
       --cov-config=tests/unit/.coveragerc \
       --cov=source/ \
       --cov=tests/ \
       --junitxml=htmlcov/junit.xml \
       -o junit_family=xunit1 \
       --pythonwarnings=ignore::pytest.PytestCollectionWarning \
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
TEST_CASES=`pytest --collect-only -q | head -n -2 | wc -l`
echo TEST_CASES=$TEST_CASES > htmlcov/test_cases.sh

#!/bin/sh

set -e

pytest --capture=no --cov=. --cov-config=.coveragerc -o junit_family=xunit2 --junitxml=htmlcov/junit.xml -v

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

#!/usr/bin/env python
import os

from junitparser import JUnitXml

from cdb.cdb_utils import parse_cmd_line, load_user_data, build_evidence_dict, \
    send_evidence


def control_junit(project_file):
    print("Publish evidence to ComplianceDB")

    junit_results_dir = os.getenv('CDB_TEST_RESULTS_DIR', '/data/junit/')

    is_compliant, message = is_compliant_tests_directory(junit_results_dir)
    evidence_type = os.getenv('CDB_EVIDENCE_TYPE', "junit")
    description = "JUnit results xml verified by compliancedb/cdb_controls: " + message
    build_url = os.getenv('CDB_CI_BUILD_URL', "URL_UNDEFINED")
    user_data = load_user_data()

    evidence = build_evidence_dict(is_compliant, evidence_type, description, build_url, user_data)
    send_evidence(project_file, evidence)


def is_compliant_suite(junit_xml):
    if junit_xml.failures != 0:
        return False, "Tests contain failures"
    if junit_xml.errors != 0:
        return False, "Tests contain errors"
    return True, "All tests passed"


def ls_test_results(root_directory):
    import glob
    files = sorted(glob.glob(root_directory + "/*.xml"))
    excluded_files = ["failsafe-summary.xml"]
    for exclude in excluded_files:
        test_files = [file for file in files if not file.endswith(exclude)]
    return test_files


def is_compliant_tests_directory(test_results_directory):
    results_files = ls_test_results(test_results_directory)
    for test_xml in results_files:
        is_compliant, message = is_compliant_test_results(test_xml)
        if not is_compliant:
            return is_compliant, message
    return True, f"All tests passed in {len(results_files)} test suites"


def load_test_results(file_path):
    test_xml = JUnitXml.fromfile(file_path)
    return test_xml


def is_compliant_test_results(file_path):
    """
    This parses a junit xml file to determine if there are any errors or failures

    return:
        A tuple, with is_compliant, plus a message string
    """
    test_xml = load_test_results(file_path)
    if test_xml._tag == "testsuites":
        for suite in test_xml:
            suite_is_compliant, message = is_compliant_suite(suite)
            if not suite_is_compliant:
                return suite_is_compliant, message
        # every test suite passed, so return True
        return True, "All tests passed"
    if test_xml._tag == "testsuite":
        return is_compliant_suite(test_xml)
    return False, "Could not find test suite(s)"


if __name__ == '__main__':
    project_file = parse_cmd_line()
    control_junit(project_file)

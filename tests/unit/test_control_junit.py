from unittest import mock

from junitparser import JUnitXml, TestCase, Skipped, Error, Failure, TestSuite

from cdb.control_junit import is_compliant_suite, ls_test_results, is_compliant_tests_directory, load_test_results, \
    is_compliant_test_results


def test_is_compliant_suite_returns_true_WHEN_no_failures_AND_no_errors_in_JUnitXML():
    # Create cases
    case1 = TestCase('case1')
    case2 = TestCase('case2')
    case2.result = [Skipped()]
    # Create suite and add cases
    suite = TestSuite('suite1')
    suite.add_property('build', '55')
    suite.add_testcase(case1)
    suite.add_testcase(case2)

    # Add suite to JunitXml
    xml = JUnitXml()
    xml.add_testsuite(suite)

    (control_result, message) = is_compliant_suite(xml)
    assert control_result is True
    assert message == "All tests passed"


def test_is_compliant_suite_returns_fails_WHEN_failures_in_JUnitXML():
    # Create cases
    case1 = TestCase('case1')
    case1.result = [Failure()]
    case2 = TestCase('case2')

    # Create suite and add cases
    suite = TestSuite('suite1')
    suite.add_property('build', '55')
    suite.add_testcase(case1)
    suite.add_testcase(case2)

    # Add suite to JunitXml
    xml = JUnitXml()
    xml.add_testsuite(suite)

    (control_result, message) = is_compliant_suite(xml)
    assert control_result is False
    assert message == "Tests contain failures"


def test_is_compliant_suite_returns_false_WHEN_errors_in_JUnitXML():
    # Create cases
    case1 = TestCase('case1')
    case1.result = [Error()]
    case2 = TestCase('case2')

    # Create suite and add cases
    suite = TestSuite('suite1')
    suite.add_property('build', '55')
    suite.add_testcase(case1)
    suite.add_testcase(case2)

    # Add suite to JunitXml
    xml = JUnitXml()
    xml.add_testsuite(suite)

    (control_result, message) = is_compliant_suite(xml)
    assert control_result is False
    assert message == "Tests contain errors"


def test_junit_parser_can_load_junit_output():
    test_xml = load_test_results('tests/unit/TEST-Junit.xml')
    # one test suite in file
    assert test_xml._tag == "testsuite"
    assert len(test_xml) == 2
    assert test_xml.failures == 1
    assert test_xml.errors == 0


def test_junit_parser_can_validate_junit_output():
    (control_result, message) = is_compliant_test_results('tests/unit/TEST-Junit.xml')
    assert control_result is False
    assert message == "Tests contain failures"


def test_junit_parser_can_load_pytest_output():
    test_xml = load_test_results('tests/unit/TEST-Pytest-pass.xml')
    # one test suite in file
    assert test_xml._tag == "testsuites"
    assert len(test_xml) == 1
    assert test_xml.failures == 0
    assert test_xml.errors == 0


def test_junit_parser_can_validate_pytest_output():
    (control_result, message) = is_compliant_test_results('tests/unit/TEST-Pytest-pass.xml')
    assert control_result is True
    assert message == "All tests passed"


def test_junit_parser_can_load_pytest_failed_output():
    test_xml = load_test_results('tests/unit/TEST-Pytest-fail.xml')
    # one test suite in file
    assert test_xml._tag == "testsuites"
    assert len(test_xml) == 1
    assert test_xml.failures == 1
    assert test_xml.errors == 0
    assert test_xml.tests == 5


def test_junit_parser_can_validate_pytest_failed_output():
    (control_result, message) = is_compliant_test_results('tests/unit/TEST-Pytest-fail.xml')
    assert control_result is False
    assert message == "Tests contain failures"


def test_junit_parser_can_load_owasp_output():
    test_xml = load_test_results('tests/unit/TEST-OWASP-pass.xml')
    # one test suite in file
    assert test_xml._tag == "testsuites"
    assert len(test_xml) == 5
    assert test_xml.failures == 0
    assert test_xml.errors == 0
    assert test_xml.tests == 5


def test_junit_parser_can_validate_owasp_output():
    (control_result, message) = is_compliant_test_results('tests/unit/TEST-OWASP-pass.xml')
    assert control_result is True
    assert message == "All tests passed"


def test_junit_parser_can_load_owasp_failed_output():
    test_xml = load_test_results('tests/unit/TEST-OWASP-fail.xml')
    # one test suite in file
    assert test_xml._tag == "testsuites"
    assert len(test_xml) == 88
    assert test_xml.failures == 26
    assert test_xml.errors == 0
    assert test_xml.tests == 106


def test_junit_parser_can_validate_owasp_failed_output():
    (control_result, message) = is_compliant_test_results('tests/unit/TEST-OWASP-fail.xml')
    assert control_result is False
    assert message == "Tests contain failures"


def test_junit_parser_can_load_surefire_output():
    test_xml = load_test_results('tests/unit/surefire_examples/TEST-com.compliancedb.example.Example1Test.xml')
    # one test suite in file
    assert test_xml._tag == "testsuite"
    # 7 testcases and one property
    assert len(test_xml) == 8
    assert test_xml.errors == 0
    assert test_xml.skipped == 0
    assert test_xml.failures == 1


def test_failing_surefire_testxml_results_in_non_compliant_evidence():
    test_xml = load_test_results('tests/unit/surefire_examples/TEST-com.compliancedb.example.Example1Test.xml')
    (control_result, message) = is_compliant_suite(test_xml)
    assert control_result is False
    assert message == "Tests contain failures"


def test_passing_surefire_testxml_results_in_compliant_evidence():
    test_xml = load_test_results('tests/unit/surefire_examples/TEST-com.compliancedb.example.Example2Test.xml')
    (control_result, message) = is_compliant_suite(test_xml)
    assert control_result is True
    assert message == "All tests passed"


def test_list_test_result_files():
    files = ls_test_results('tests/unit/surefire_examples/')
    assert files == ['tests/unit/surefire_examples/TEST-com.compliancedb.example.Example1Test.xml',
                     'tests/unit/surefire_examples/TEST-com.compliancedb.example.Example2Test.xml']


def test_list_test_result_files_filters_failsafe_summary_xml():
    files = ls_test_results('tests/unit/failsafe_examples/')
    assert files == ['tests/unit/failsafe_examples/TEST-com.compliancedb.example.Example1Test.xml']


@mock.patch('cdb.control_junit.is_compliant_test_results')
@mock.patch('cdb.control_junit.ls_test_results')
def test_is_compliant_tests_directory_passes_if_every_file_has_no_failures(mocked_ls, mocked_results):
    mocked_ls.return_value = \
        ['tests/unit/surefire_examples/TEST-com.compliancedb.example.Example1Test.xml',
         'tests/unit/surefire_examples/TEST-com.compliancedb.example.Example2Test.xml']

    mocked_results.side_effect = [(True, "All good"), (True, "All good")]
    (result, message) = is_compliant_tests_directory("tests/unit/surefire_examples")

    assert mocked_results.call_count == 2
    assert result
    assert message == "All tests passed in 2 test suites"


@mock.patch('cdb.control_junit.is_compliant_test_results')
@mock.patch('cdb.control_junit.ls_test_results')
def test_is_compliant_tests_directory_fails_if_a_file_has_failures(mocked_ls, mocked_results):
    mocked_ls.return_value = \
        ['tests/unit/surefire_examples/TEST-com.compliancedb.example.Example1Test.xml',
         'tests/unit/surefire_examples/TEST-com.compliancedb.example.Example2Test.xml']

    mocked_results.side_effect = [(True, "All good"), (False, "Bad stuff")]
    (result, message) = is_compliant_tests_directory("tests/unit/surefire_examples")

    assert mocked_results.call_count == 2
    assert result is False
    assert message == "Bad stuff"


def test_passing_failsafe_testxml_results_in_compliant_evidence():
    test_xml = load_test_results('tests/unit/failsafe_examples/TEST-com.compliancedb.example.Example1Test.xml')
    (control_result, message) = is_compliant_suite(test_xml)
    assert control_result is True
    assert message == "All tests passed"

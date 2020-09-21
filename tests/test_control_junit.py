from junitparser import JUnitXml, TestCase, Skipped, Error, Failure, TestSuite

from cdb.cdb_utils import is_compliant_suite, load_test_results, is_compliant_test_results


def test_junit_parser_control_passes_WHEN_no_failures_AND_no_errors():
    # Create cases
    case1 = TestCase('case1')
    case2 = TestCase('case2')
    case2.result = Skipped()
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


def test_junit_parser_control_fails_WHEN_failures():
    # Create cases
    case1 = TestCase('case1')
    case1.result = Failure()
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


def test_junit_parser_control_fails_WHEN_errors():
    # Create cases
    case1 = TestCase('case1')
    case1.result = Error()
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
    test_xml = load_test_results('tests/TEST-Junit.xml')
    # one test suite in file
    assert test_xml._tag == "testsuite"
    assert len(test_xml) == 2
    assert test_xml.failures == 1
    assert test_xml.errors == 0


def test_junit_parser_can_validate_junit_output():
    (control_result, message) = is_compliant_test_results('tests/TEST-Junit.xml')
    assert control_result is False
    assert message == "Tests contain failures"


def test_junit_parser_can_load_pytest_output():
    test_xml = load_test_results('tests/TEST-Pytest-pass.xml')
    # one test suite in file
    assert test_xml._tag == "testsuites"
    assert len(test_xml) == 1
    assert test_xml.failures == 0
    assert test_xml.errors == 0


def test_junit_parser_can_validate_pytest_output():
    (control_result, message) = is_compliant_test_results('tests/TEST-Pytest-pass.xml')
    assert control_result is True
    assert message == "All tests passed"


def test_junit_parser_can_load_pytest_failed_output():
    test_xml = load_test_results('tests/TEST-Pytest-fail.xml')
    # one test suite in file
    assert test_xml._tag == "testsuites"
    assert len(test_xml) == 1
    assert test_xml.failures == 1
    assert test_xml.errors == 0
    assert test_xml.tests == 5


def test_junit_parser_can_validate_pytest_failed_output():
    (control_result, message) = is_compliant_test_results('tests/TEST-Pytest-fail.xml')
    assert control_result is False
    assert message == "Tests contain failures"


def test_junit_parser_can_load_owasp_output():
    test_xml = load_test_results('tests/TEST-OWASP-pass.xml')
    # one test suite in file
    assert test_xml._tag == "testsuites"
    assert len(test_xml) == 5
    assert test_xml.failures == 0
    assert test_xml.errors == 0
    assert test_xml.tests == 5


def test_junit_parser_can_validate_owasp_output():
    (control_result, message) = is_compliant_test_results('tests/TEST-OWASP-pass.xml')
    assert control_result is True
    assert message == "All tests passed"


def test_junit_parser_can_load_owasp_failed_output():
    test_xml = load_test_results('tests/TEST-OWASP-fail.xml')
    # one test suite in file
    assert test_xml._tag == "testsuites"
    assert len(test_xml) == 88
    assert test_xml.failures == 26
    assert test_xml.errors == 0
    assert test_xml.tests == 106


def test_junit_parser_can_validate_owasp_failed_output():
    (control_result, message) = is_compliant_test_results('tests/TEST-OWASP-fail.xml')
    assert control_result is False
    assert message == "Tests contain failures"

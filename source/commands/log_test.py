from commands import Command
from docs import *
from env_vars import *
from errors import ChangeError
from lib.api_schema import ApiSchema
from junitparser import JUnitXml, JUnitXmlError
import os
import glob


class LogTest(Command):

    def doc_summary(self, _ci_name):
        return " ".join([
            "Logs JUnit xml format test summary evidence in Merkely.",
            "The JUnit xml format is used by many tools, not just testing frameworks.",
            f"By default, looks for JUnit .xml files in the {self.default_test_results_dir} dir."
        ])

    def doc_volume_mounts(self, ci_name):
        if ci_name == 'docker':
            return [
                f"${{YOUR_TEST_RESULTS_DIR}}:{self.default_test_results_dir}",
                "/var/run/docker.sock:/var/run/docker.sock",
            ]
        else:
            return []

    def doc_ref(self):
        return {
            'docker': (docker_change_makefile_line_ref, 'merkely_log_test:'),
            'github': (github_loan_calculator_master_pipeline_line_ref, 'MERKELY_COMMAND: log_test'),
            'bitbucket': (bitbucket_loan_calculator_line_ref, 'MERKELY_COMMAND: log_test'),
        }

    def __call__(self):
        url = ApiSchema.url_for_artifact(self.host.value, self.merkelypipe, self.fingerprint.sha)
        junit_results_dir = self.test_results_dir.value
        is_compliant, message = is_compliant_tests_directory(junit_results_dir)
        setattr(self, 'default_suffix', message)
        payload = {
            "evidence_type": self.evidence_type.value,
            "user_data": self.user_data.value,
            "contents": {
                "is_compliant": is_compliant,
                "url": self.ci_build_url.value,
                "description": self.description.value
            }
        }
        return 'PUT', url, payload, None

    @property
    def description(self):
        prefix = "JUnit results xml verified by merkely/change: "
        suffix = getattr(self, 'default_suffix', 'All tests passed in 1 test suites')
        return DescriptionEnvVar(self.env, prefix, suffix)

    @property
    def evidence_type(self):
        return EvidenceTypeEnvVar(self.env)

    @property
    def test_results_dir(self):
        return TestResultsDirEnvVar(self.env)

    @property
    def _merkely_env_var_names(self):
        # In docs print in this order
        return [
            'name',
            'fingerprint',
            'evidence_type',
            'test_results_dir',
            'description',
            'ci_build_url',
            'user_data',
            'owner',
            'pipeline',
            'api_token',
            'host',
            'dry_run'
        ]

    @property
    def default_test_results_dir(self):
        return self.test_results_dir.default


class DescriptionEnvVar(StaticDefaultedEnvVar):

    def __init__(self, env, default_prefix, default_suffix):
        default = default_prefix + default_suffix
        self._default_prefix = default_prefix
        self._default_suffix = default_suffix
        super().__init__(env, "MERKELY_DESCRIPTION", default)

    def doc_example(self, _ci_name, _command_name):
        return False, ""

    def doc_note(self, _ci_name, _command_name):
        return " ".join([
            "A description of the test summary.",
            f'Defaults to "{self._default_prefix}"',
            f'followed by a summary, eg "{self._default_suffix}"'
        ])

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def is_compliant_tests_directory(test_results_directory):
    results_files = ls_test_results(test_results_directory)
    if len(results_files) == 0:
        raise ChangeError(f"No test suites in {test_results_directory}")

    for test_xml in results_files:
        is_compliant, message = is_compliant_test_results(test_xml)
        if not is_compliant:
            return is_compliant, message
    return True, f"All tests passed in {len(results_files)} test suites"


def ls_test_results(root_directory):
    if not os.path.isdir(root_directory):
        raise ChangeError(f"no directory {root_directory}")
    files = sorted(glob.glob(root_directory + "/*.xml"))
    excluded_files = ["failsafe-summary.xml"]
    for exclude in excluded_files:
        test_files = [file for file in files if not file.endswith(exclude)]
    return test_files


def is_compliant_test_results(file_path):
    """
    This parses a junit xml file to determine if there are any errors or failures

    return:
        A tuple, with is_compliant, plus a message string
    """
    try:
        test_xml = JUnitXml.fromfile(file_path)
    except JUnitXmlError:
        raise ChangeError(f"XML file {file_path} not JUnit format.")
    if test_xml._tag == "testsuites":
        for suite in test_xml:
            suite_is_compliant, message = is_compliant_suite(suite)
            if not suite_is_compliant:
                return suite_is_compliant, message
        # every test suite passed, so return True
        return True, "All tests passed"
    if test_xml._tag == "testsuite":
        return is_compliant_suite(test_xml)


def is_compliant_suite(junit_xml):
    if junit_xml.failures != 0:
        return False, "Tests contain failures"
    if junit_xml.errors != 0:
        return False, "Tests contain errors"
    return True, "All tests passed"



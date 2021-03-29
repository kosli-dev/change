from errors import ChangeError
from commands import Command
from env_vars import *
from cdb.api_schema import ApiSchema
from junitparser import JUnitXml

DEFAULT_TEST_DIR = "/data/junit/"


class LogTest(Command):

    def summary(self, _ci):
        return " ".join([
            "Logs JUnit xml format test summary evidence in Merkely.",
            f"By default, looks for JUnit .xml files in the dir {DEFAULT_TEST_DIR}"
        ])

    def volume_mounts(self, ci):
        mounts = ["${YOUR_TEST_RESULTS_DIR}:/data/junit"]
        if ci != 'bitbucket':
            mounts.append("/var/run/docker.sock:/var/run/docker.sock")
        return mounts

    def __call__(self):
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
        url = ApiSchema.url_for_artifact(self.host.value, self.merkelypipe, self.fingerprint.sha)
        return 'Putting', url, payload, None

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
        ]


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
            "A description of the test.",
            f'Defaults to "{self._default_prefix}"',
            f'followed by the JUnit .xml summary, eg "{self._default_suffix}"'
        ])


class TestResultsDirEnvVar(StaticDefaultedEnvVar):
    
    def __init__(self, env):
        super().__init__(env, "MERKELY_TEST_RESULTS_DIR", DEFAULT_TEST_DIR)

    def doc_example(self, ci_name, _command_name):
        if ci_name == 'github':
            return True, "${{ github.workspace }}/build/test"
        if ci_name == 'bitbucket':
            return True, "${PWD}/build/test/"
        return False, ""

    def doc_note(self, _ci_name, _command_name):
        return " ".join([
            "The directory where Merkely will look for JUnit .xml files.",
            "Must be volume-mounted in the container.",
            f"Defaults to {DEFAULT_TEST_DIR}"
        ])

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def is_compliant_suite(junit_xml):
    if junit_xml.failures != 0:
        return False, "Tests contain failures"
    if junit_xml.errors != 0:
        return False, "Tests contain errors"
    return True, "All tests passed"


def is_compliant_tests_directory(test_results_directory):
    results_files = ls_test_results(test_results_directory)
    for test_xml in results_files:
        is_compliant, message = is_compliant_test_results(test_xml)
        if not is_compliant:
            return is_compliant, message
    return True, f"All tests passed in {len(results_files)} test suites"


def ls_test_results(root_directory):
    import os
    if not os.path.isdir(root_directory):
        raise ChangeError(f"no directory {root_directory}")
    import glob
    files = sorted(glob.glob(root_directory + "/*.xml"))
    excluded_files = ["failsafe-summary.xml"]
    for exclude in excluded_files:
        test_files = [file for file in files if not file.endswith(exclude)]
    return test_files


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

from errors import ChangeError
from commands import Command
from env_vars import *
from cdb.api_schema import ApiSchema
from cdb.http import http_put_payload
from cdb.control_junit import is_compliant_test_results

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
        description = "JUnit results xml verified by merkely/change: " + message
        payload = {
            "evidence_type": self.evidence_type.value,
            "user_data": self.user_data.value,
            "contents": {
                "is_compliant": is_compliant,
                "url": self.ci_build_url.value,
                "description": description
            }
        }
        url = ApiSchema.url_for_artifact(self.host.value, self.merkelypipe, self.fingerprint.sha)
        http_put_payload(url, payload, self.api_token.value)
        return 'Putting', url, payload

    @property
    def evidence_type(self):
        return EvidenceTypeEnvVar(self.env)

    @property
    def test_results_dir(self):
        return TestResultsDirEnvVar(self.env)

    @property
    def _merkely_env_var_names(self):
        # Print in this order
        return [
            'name',
            'fingerprint',
            'evidence_type',
            'test_results_dir',
            'ci_build_url',
            'user_data',
            'owner',
            'pipeline',
            'api_token',
            'host',
        ]


class TestResultsDirEnvVar(StaticDefaultedEnvVar):
    def __init__(self, env):
        notes = " ".join([
            "The directory where Merkely will look for JUnit .xml files.",
            "Must be volume-mounted in the container.",
            f"Defaults to {DEFAULT_TEST_DIR}"
        ])
        super().__init__(env, "MERKELY_TEST_RESULTS_DIR", DEFAULT_TEST_DIR, notes)

    def ci_doc_example(self, ci_name, _command_name):
        if ci_name == 'github':
            return True, "${{ github.workspace }}/build/security"
        return False, ""


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


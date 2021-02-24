from errors import ChangeError
from commands import Command
from env_vars import *
from cdb.api_schema import ApiSchema
from cdb.http import http_put_payload
from cdb.control_junit import is_compliant_test_results


class LogTest(Command):

    @property
    def summary(self):
        return "".join([
            "Logs JUnit xml test summary evidence in Merkely.",
            "The JUnit xml file(s) must be volume-mounted to /data/junit/*.xml"
        ])

    @property
    def _volume_mounts(self):
        return [
            "${TEST_RESULTS_FILE}:/data/junit/junit.xml"
            "/var/run/docker.sock:/var/run/docker.sock"
        ]

    def __call__(self):
        junit_results_dir = '/data/junit/'
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
        notes = "The evidence type."
        return self._required_env_var("MERKELY_EVIDENCE_TYPE", notes)

    @property
    def _env_var_names(self):
        # Print according to this order
        return [
            'name',
            'fingerprint',
            'evidence_type',
            'ci_build_url',
            'user_data',
            'api_token',
            'host',
        ]


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


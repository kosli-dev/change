from commands import Command
from cdb.api_schema import ApiSchema
from cdb.http import http_put_payload
from cdb.control_junit import is_compliant_test_results


class LogTestCommand(Command):

    @property
    def summary(self):
        return "Logs test evidence in Merkely."

    def invocation(self, type):
        def env(var):
            if var.name == "MERKELY_COMMAND":
                value = var.value
            elif var.name == "MERKELY_FINGERPRINT":
                value = var.example
            else:
                value = "${...}"
            return f'    --env {var.name}="{value}" \\\n'

        invocation_string = "docker run \\\n"
        for name in self._env_var_names:
            var = getattr(self, name)
            if type == 'full':
                invocation_string += env(var)
            if type == 'minimum' and var.is_required:
                invocation_string += env(var)

        invocation_string += "    --rm \\\n"
        invocation_string += "    --volume /var/run/docker.sock:/var/run/docker.sock \\\n"
        invocation_string += "    --volume ${YOUR_MERKELY_PIPE}:/Merkelypipe.json \\\n"
        invocation_string += "    merkely/change"
        return invocation_string

    def __call__(self):
        # Notes
        # 1) junit_results_dir was read from ev CDB_TEST_RESULTS_DIR
        #       with '/data/junit/' as a default
        #    The merkely_log_test makefile target now does this
        # 		--volume ${MERKELY_TEST_RESULTS_FILE}:/data/junit/junit.xml \
        # 2) user_data was read from ev CDB_USER_DATA
        #       as json with None as default
        #    No equivalent env-var for that yet.
        junit_results_dir = '/data/junit/'
        is_compliant, message = is_compliant_tests_directory(junit_results_dir)
        description = "JUnit results xml verified by compliancedb/cdb_controls: " + message
        user_data = None  # cbd.cbd_utils.load_user_data()

        payload = {
            "evidence_type": self.evidence_type.value,
            "contents": {
                "is_compliant": is_compliant,
                "url": self.ci_build_url.value,
                "description": description
            }
        }
        if user_data is not None:
            payload["user_data"]: user_data

        url = ApiSchema.url_for_artifact(self.host.value, self.merkelypipe, self.fingerprint.sha)
        http_put_payload(url, payload, self.api_token.value)
        return 'Putting', url, payload

    @property
    def ci_build_url(self):
        notes = "Link to the build information."
        return self._required_env_var('CI_BUILD_URL', notes)

    @property
    def evidence_type(self):
        notes = "The evidence type."
        return self._required_env_var("EVIDENCE_TYPE", notes)

    @property
    def _env_var_names(self):
        # Print according to this order
        return [
            'name',
            'fingerprint',
            'evidence_type',
            'ci_build_url',
            'api_token',
            'host',
        ]


def is_compliant_tests_directory(test_results_directory):
    #import pdb
    #pdb.set_trace()
    results_files = ls_test_results(test_results_directory)
    for test_xml in results_files:
        is_compliant, message = is_compliant_test_results(test_xml)
        if not is_compliant:
            return is_compliant, message
    return True, f"All tests passed in {len(results_files)} test suites"


def ls_test_results(root_directory):
    import glob
    files = sorted(glob.glob(root_directory + "/*.xml"))
    excluded_files = ["failsafe-summary.xml"]
    for exclude in excluded_files:
        test_files = [file for file in files if not file.endswith(exclude)]
    return test_files

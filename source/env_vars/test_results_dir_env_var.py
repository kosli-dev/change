from env_vars import StaticDefaultedEnvVar

DEFAULT_TEST_RESULTS_DIR = "/data/junit/"


class TestResultsDirEnvVar(StaticDefaultedEnvVar):

    def __init__(self, env):
        super().__init__(env, "MERKELY_TEST_RESULTS_DIR", DEFAULT_TEST_RESULTS_DIR)

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
            f"Defaults to :code:`{DEFAULT_TEST_RESULTS_DIR}`"
        ])

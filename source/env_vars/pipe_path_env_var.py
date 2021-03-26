from env_vars import StaticDefaultedEnvVar

DEFAULT = "/data/Merkelypipe.json"


class PipePathEnvVar(StaticDefaultedEnvVar):

    def __init__(self, env):
        super().__init__(env, "MERKELY_PIPE_PATH", DEFAULT)

    def doc_example(self, ci_name, _command_name):
        if ci_name == 'github':
            return True, "${{ github.workspace }}/Merkelypipe.json"
        if ci_name == 'bitbucket':
            return True, "${MERKELY_PIPE_PATH}"
        return False, ""

    def doc_note(self, _ci_name, _command_name):
        return " ".join([
            f"The full path to your Merkelypipe file.",
            "Must be volume-mounted in the container.",
            f"Defaults to {DEFAULT}.",
        ])


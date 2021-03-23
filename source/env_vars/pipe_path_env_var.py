from env_vars import StaticDefaultedEnvVar

NAME = "MERKELY_PIPE_PATH"
DEFAULT = "/data/Merkelypipe.json"
NOTES = " ".join([
    f"The full path to your Merkelypipe file.",
    "Must be volume-mounted in the container.",
    f"Defaults to {DEFAULT}.",
])


class PipePathEnvVar(StaticDefaultedEnvVar):

    def __init__(self, env):
        super().__init__(env, "MERKELY_PIPE_PATH", DEFAULT, NOTES)

    def ci_doc_example(self, ci_name, _command_name):
        if ci_name == 'github':
            return True, "${{ github.workspace }}/Merkelypipe.json"
        if ci_name == 'bitbucket':
            return True, "${MERKELY_PIPE_PATH}"
        return False, ""

from env_vars import StaticDefaultedEnvVar

DEFAULT_HOST = "https://app.merkely.com"


class HostEnvVar(StaticDefaultedEnvVar):

    def __init__(self, env):
        super().__init__(env, "MERKELY_HOST", DEFAULT_HOST)

    def doc_example(self, _ci_name, _command_name):
        return False, ""

    def doc_note(self, _ci_name, _command_name):
        return " ".join([
            "The API hostname for Merkely.",
            f"Defaults to :code:`{DEFAULT_HOST}`",
        ])

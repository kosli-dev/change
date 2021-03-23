from env_vars import StaticDefaultedEnvVar

DEFAULT = "https://app.compliancedb.com"

NOTES = " ".join([
    "The API hostname for Merkely.",
    f"Defaults to {DEFAULT}",
])


class HostEnvVar(StaticDefaultedEnvVar):

    def __init__(self, env):
        super().__init__(env, "MERKELY_HOST", DEFAULT, NOTES)

    def ci_doc_example(self, ci_name, _command_name):
        return False, ""

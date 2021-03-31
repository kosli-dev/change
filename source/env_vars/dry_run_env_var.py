from env_vars import StaticDefaultedEnvVar

DEFAULT = '"FALSE'

class DryRunEnvVar(StaticDefaultedEnvVar):

    def __init__(self, env):
        super().__init__(env, "MERKELY_DRY_RUN", DEFAULT)

    def doc_example(self, _ci_name, _command_name):
        return False, ""

    def doc_note(self, _ci_name, _command_name):
        return " ".join([
            "...TODO...",
            f"Defaults to {DEFAULT}",
        ])

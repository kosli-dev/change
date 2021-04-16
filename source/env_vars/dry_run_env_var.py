from env_vars import StaticDefaultedEnvVar

DEFAULT = '"FALSE"'


class DryRunEnvVar(StaticDefaultedEnvVar):

    def __init__(self, env):
        super().__init__(env, "MERKELY_DRY_RUN", DEFAULT)

    def doc_example(self, _ci_name, _command_name):
        return False, ""

    def doc_note(self, _ci_name, _command_name):
        return " ".join([
            'When set to :code:`"TRUE"`, prints the command\'s url+payload,',
            "does not make any HTTP calls to Merkely,",
            "and exits the command with a zero status code.",
            f"Defaults to :code:`{DEFAULT}`.",
            "See also setting the MERKELY_API_TOKEN (above) to code:`DRY_RUN`."
        ])

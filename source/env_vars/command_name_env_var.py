from env_vars import RequiredEnvVar


class CommandNameEnvVar(RequiredEnvVar):

    def __init__(self, env):
        super().__init__(env, "MERKELY_COMMAND", '')

    def doc_example(self, ci_name, command_name):
        return True, command_name

    def doc_note(self, _ci_name, command_name):
        return " ".join([
            "The Merkely command to execute.",
            f"This page documents a value of `{command_name}`"
        ])

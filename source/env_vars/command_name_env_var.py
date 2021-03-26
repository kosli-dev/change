from env_vars import RequiredEnvVar


class CommandNameEnvVar(RequiredEnvVar):

    def __init__(self, env):
        notes = "The Merkely command to execute."
        super().__init__(env, "MERKELY_COMMAND", notes)

    def doc_example(self, ci_name, command_name):
        return True, command_name

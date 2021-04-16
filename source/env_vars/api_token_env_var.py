from env_vars import RequiredEnvVar


class ApiTokenEnvVar(RequiredEnvVar):

    def __init__(self, env):
        super().__init__(env, "MERKELY_API_TOKEN")

    def doc_example(self, ci_name, _command_name):
        if ci_name == 'github':
            return True, "${{ secrets.MERKELY_API_TOKEN }}"
        if ci_name == 'bitbucket':
            return True, "${MERKELY_API_TOKEN}"
        return False, ""

    def doc_note(self, _ci_name, _command_name):
        return " ".join([
            "Your secret API token for Merkely.",
            'Set this to :code:`"DRY_RUN"` to turn off all commands in all pipelines.',
        ])

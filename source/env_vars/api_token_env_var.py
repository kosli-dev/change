from env_vars import RequiredEnvVar

NOTES = "Your API token for Merkely."


class ApiTokenEnvVar(RequiredEnvVar):

    def __init__(self, env):
        super().__init__(env, "MERKELY_API_TOKEN", NOTES)

    def ci_doc_example(self, ci_name, _command_name):
        if ci_name == 'github':
            return True, "${{ secrets.MERKELY_API_TOKEN }}"
        if ci_name == 'bitbucket':
            return True, "${MERKELY_API_TOKEN}"
        return False, ""

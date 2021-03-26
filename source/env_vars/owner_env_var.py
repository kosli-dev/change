from env_vars import RequiredEnvVar


class OwnerEnvVar(RequiredEnvVar):

    def __init__(self, env):
        super().__init__(env, "MERKELY_OWNER", '')

    def doc_example(self, ci_name, _command_name):
        if ci_name == 'github':
            return True, "${{ env.MERKELY_OWNER }}"
        if ci_name == 'bitbucket':
            return True, "${MERKELY_OWNER}"
        return False, ""

    def doc_note(self, _ci_name, _command_name):
        return "Your user/organization name in Merkely."

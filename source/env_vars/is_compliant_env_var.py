from env_vars import RequiredEnvVar


class IsCompliantEnvVar(RequiredEnvVar):

    def __init__(self, env):
        super().__init__(env, "MERKELY_IS_COMPLIANT")

    def doc_example(self, ci_name, _command_name):
        if ci_name == 'github':
            return True, '"TRUE"'
        if ci_name == 'bitbucket':
            return True, '"TRUE"'
        return False, ""

    def doc_note(self, _ci_name, _command_name):
        return "TRUE if the artifact is considered compliant from you build process."

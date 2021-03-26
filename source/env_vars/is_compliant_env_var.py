from env_vars import RequiredEnvVar

NOTES = "TRUE if the artifact is considered compliant from you build process."


class IsCompliantEnvVar(RequiredEnvVar):

    def __init__(self, env):
        super().__init__(env, "MERKELY_IS_COMPLIANT", NOTES)

    def doc_example(self, ci_name, _command_name):
        if ci_name == 'github':
            return True, '"TRUE"'
        if ci_name == 'bitbucket':
            return True, '"TRUE"'
        return False, ""

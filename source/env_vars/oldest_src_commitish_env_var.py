from env_vars import RequiredEnvVar


class OldestSrcCommitishEnvVar(RequiredEnvVar):

    def __init__(self, env):
        super().__init__(env, "MERKELY_OLDEST_SRC_COMMITISH", '')

    def doc_example(self, ci_name, _command_name):
        if ci_name == 'github':
            return True, "origin/production"
        if ci_name == 'bitbucket':
            return True, '"origin/production"'
        return False, ""

    def doc_note(self, _ci_name, _command_name):
        return "The source commit-ish for the oldest change in the approval."

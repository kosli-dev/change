from env_vars import RequiredEnvVar


class OldestSrcCommitishEnvVar(RequiredEnvVar):

    def __init__(self, env):
        notes = "The source commit-ish for the oldest change in the approval."
        super().__init__(env, "MERKELY_OLDEST_SRC_COMMITISH", notes)

    def doc_example(self, ci_name, _command_name):
        if ci_name == 'github':
            return True, "origin/production"
        if ci_name == 'bitbucket':
            return True, '"origin/production"'
        return False, ""


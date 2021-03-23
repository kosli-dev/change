from env_vars import RequiredEnvVar

NOTES = "The source commit-ish for the newest change in the approval."


class NewestSrcCommitishEnvVar(RequiredEnvVar):

    def __init__(self, env):
        super().__init__(env, "MERKELY_NEWEST_SRC_COMMITISH", NOTES)

    def ci_doc_example(self, ci_name, _command_name):
        if ci_name == 'github':
            return True, "${{ github.event.inputs.deploy_commit }}"
        if ci_name == 'bitbucket':
            return True, "${BITBUCKET_COMMIT}"
        return False, ""


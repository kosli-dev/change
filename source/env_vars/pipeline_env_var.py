from env_vars import RequiredEnvVar


class PipelineEnvVar(RequiredEnvVar):

    def __init__(self, env):
        notes = "Your pipeline name inside your user/organization in Merkely."
        super().__init__(env, "MERKELY_PIPELINE", notes)

    def doc_example(self, ci_name, _command_name):
        if ci_name == 'github':
            return True, "${{ env.MERKELY_PIPELINE }}"
        if ci_name == 'bitbucket':
            return True, "${MERKELY_PIPELINE}"
        return False, ""

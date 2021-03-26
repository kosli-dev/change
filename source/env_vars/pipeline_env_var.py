from env_vars import RequiredEnvVar


class PipelineEnvVar(RequiredEnvVar):

    def __init__(self, env):
        super().__init__(env, "MERKELY_PIPELINE", '')

    def doc_example(self, ci_name, _command_name):
        if ci_name == 'github':
            return True, "${{ env.MERKELY_PIPELINE }}"
        if ci_name == 'bitbucket':
            return True, "${MERKELY_PIPELINE}"
        return False, ""

    def doc_note(self, _ci_name, _command_name):
        return "Your pipeline name in your user/organization in Merkely."

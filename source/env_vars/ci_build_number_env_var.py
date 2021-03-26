from env_vars import CompoundEnvVar, CompoundCiEnvVar, CiEnvVar


class CIBuildNumberEnvVar(CompoundCiEnvVar):

    def __init__(self, env):
        super().__init__(env, "MERKELY_CI_BUILD_NUMBER")

    @property
    def _ci_env_vars(self):
        return {
            'bitbucket': CompoundEnvVar(self._env, self.name, CiEnvVar('BITBUCKET_BUILD_NUMBER')),
            'github': CompoundEnvVar(self._env, self.name, CiEnvVar('GITHUB_RUN_ID')),
        }

    def doc_example(self, _ci_name, _command_name):
        return False, ""

    def doc_note(self, _ci_name, _command_name):
        return "The ci build number."


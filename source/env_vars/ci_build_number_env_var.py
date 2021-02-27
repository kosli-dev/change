from env_vars import CompoundEnvVar, DynamicCiEnvVar, CiEnvVar

NAME = "MERKELY_CI_BUILD_NUMBER"
NOTE = "The ci build number."


class CIBuildNumberEnvVar(DynamicCiEnvVar):

    def __init__(self, env):
        super().__init__(env, NAME, NOTE)

    @property
    def _ci_env_vars(self):
        return {
            'bitbucket': CompoundEnvVar(self._env, self.name, CiEnvVar('BITBUCKET_BUILD_NUMBER')),
            'github': CompoundEnvVar(self._env, self.name, CiEnvVar('GITHUB_RUN_ID')),
        }

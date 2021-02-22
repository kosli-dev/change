from env_vars import CompoundEnvVar, DynamicEnvVar

NAME = "MERKELY_CI_BUILD_NUMBER"
NOTE = "The ci build number."


class CIBuildNumberEnvVar(DynamicEnvVar):

    def __init__(self, env):
        super().__init__(env, NAME, NOTE)

    @property
    def _ci_env_vars(self):
        return {
            'bitbucket': CompoundEnvVar(self._env, self.name, '${BITBUCKET_BUILD_NUMBER}'),
            'github': CompoundEnvVar(self._env, self.name, '${GITHUB_RUN_ID}'),
        }

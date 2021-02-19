from env_vars import CompoundEnvVar, DefaultedEnvVar

NAME = "MERKELY_CI_BUILD_NUMBER"
NOTE = "The ci build number."


class CIBuildNumberEnvVar(DefaultedEnvVar):

    def __init__(self, env):
        super().__init__(env, NAME, '')

    def notes(self, ci):
        #return f"{NOTE}. Defaults to {self._ci_env_var.string}."
        return NOTE

    @property
    def is_required(self):
        return True  # To keep Docs the same for now

    @property
    def value(self):
        if self.is_set:
            return self.string
        else:
            return self._ci_env_var.value

    @property
    def _ci_env_var(self):
        return {
            'bitbucket': CompoundEnvVar(self._env, self.name, '${BITBUCKET_BUILD_NUMBER}'),
            'github': CompoundEnvVar(self._env, self.name, '${GITHUB_RUN_ID}'),
        }[self._ci]

    @property
    def _ci(self):
        #return 'bitbucket'
        return 'github'

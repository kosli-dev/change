from env_vars import CompoundEnvVar, DefaultedEnvVar

NAME = "MERKELY_ARTIFACT_GIT_COMMIT"
NOTE = "The sha of the git commit that produced this build."


class ArtifactGitCommitEnvVar(DefaultedEnvVar):

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
            'bitbucket': CompoundEnvVar(self._env, self.name, '${BITBUCKET_COMMIT}'),
            'github': CompoundEnvVar(self._env, self.name, '${GITHUB_SHA}'),
        }[self._ci]

    @property
    def _ci(self):
        return 'github'
        #return 'bitbucket'

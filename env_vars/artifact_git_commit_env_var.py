from env_vars import DefaultedEnvVar

CI_ENV_VAR_NAMES = {
    'bitbucket': 'BITBUCKET_COMMIT',
    'github': 'GITHUB_SHA',
}
NOTE = "The sha of the git commit that produced this build."
NOTES = "\n".join([
    NOTE,
    #"On Github, defaults to ${GITHUB_SHA}.",
    #"On BitBucket, defaults to ${BITBUCKET_COMMIT}."
])


class ArtifactGitCommitEnvVar(DefaultedEnvVar):

    def __init__(self, env):
        super().__init__(env, "ARTIFACT_GIT_COMMIT", '')

    def notes(self, ci):
        def bash(s):
            return "${"+s+"}"
        #return f"{NOTE}. Defaults to {bash(CI_ENV_VAR_NAMES[ci])}."
        return NOTES

    @property
    def is_required(self):
        return True  # To keep Docs the same for now

    @property
    def value(self):
        if self.is_set:
            return self.string
        for env_var_name in CI_ENV_VAR_NAMES.values():
            value = self._get(name=env_var_name, default=None)
            if value is not None:
                return value
        # Error if both are set

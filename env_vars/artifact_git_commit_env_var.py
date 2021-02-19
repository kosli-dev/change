from env_vars import DefaultedEnvVar


class ArtifactGitCommitEnvVar(DefaultedEnvVar):

    def __init__(self, env):
        super().__init__(env, "ARTIFACT_GIT_COMMIT", '')

    def notes(self, ci):
        note = "The sha of the git commit that produced this build"
        default = {
            'bitbucket': 'BITBUCKET_COMMIT',
            'github': 'GITHUB_SHA',
        }[ci]
        return f"{note}. Defaults to ${{{default}}}."

    @property
    def value(self):
        if self.is_set:
            return self.string
        bit_bucket = self._get(name="BITBUCKET_COMMIT", default=None)
        if bit_bucket is not None:
            return bit_bucket
        github = self._get(name="GITHUB_SHA", default=None)
        if github is not None:
            return github
        # Error if both are set

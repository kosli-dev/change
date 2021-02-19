from env_vars import DefaultedEnvVar

NOTES = "\n".join([
    "The sha of the git commit that produced this build.",
    "If explicitly set, no defaults are applied.",
    "If not set, and the BitBucket BITBUCKET_COMMIT env-var exists, it is used.",
    "If not set, and the Github, GITHUB_SHA env-var exists, it is used.",
])


class ArtifactGitCommitEnvVar(DefaultedEnvVar):

    def __init__(self, env):
        super().__init__(env, "ARTIFACT_GIT_COMMIT", NOTES)

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

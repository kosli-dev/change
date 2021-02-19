from env_vars import DefaultedEnvVar

NOTES = "\n".join([
    "The ci build number."
    #"On Github, defaults to ${GITHUB_RUN_ID}.",
    #"On BitBucket, defaults to ${BITBUCKET_BUILD_NUMBER}."
])

DEFAULTS = {
    'bitbucket': 'BITBUCKET_BUILD_NUMBER',
    'github': 'GITHUB_RUN_ID',
}

class CIBuildNumberEnvVar(DefaultedEnvVar):

    def __init__(self, env):
        super().__init__(env, "CI_BUILD_NUMBER", '')

    def notes(self, ci):
        def bash(s):
            return "${"+s+"}"
        #return f"{note}. Defaults to {bash(DEFAULTS[ci])}."
        return NOTES

    @property
    def is_required(self):
        return True  # To keep Docs the same for now

    @property
    def value(self):
        if self.is_set:
            return self.string
        bit_bucket = self._get(name="BITBUCKET_BUILD_NUMBER", default=None)
        if bit_bucket is not None:
            return bit_bucket
        github = self._get(name="GITHUB_RUN_ID", default=None)
        if github is not None:
            return github
        # Error if both are set

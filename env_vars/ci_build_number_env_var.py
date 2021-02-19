from env_vars import DefaultedEnvVar

CI_ENV_VAR_NAMES = {
    'bitbucket': 'BITBUCKET_BUILD_NUMBER',
    'github': 'GITHUB_RUN_ID',
}
NOTE = "The ci build number."
NOTES = "\n".join([
    NOTE,
    #"On Github, defaults to ${GITHUB_RUN_ID}.",
    #"On BitBucket, defaults to ${BITBUCKET_BUILD_NUMBER}."
])


class CIBuildNumberEnvVar(DefaultedEnvVar):

    def __init__(self, env):
        super().__init__(env, "CI_BUILD_NUMBER", '')

    def notes(self, ci):
        def bash(s):
            return "${"+s+"}"
        #return f"{NOTE}. Defaults to {bash(CI_ENV_VAR_NAMES[ci])}."
        return NOTE

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

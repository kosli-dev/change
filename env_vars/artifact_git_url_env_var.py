from env_vars import DefaultedEnvVar

NOTE = "The link to the source git commit this build was based on."

CI_ENV_VAR_NAMES = {
    'bitbucket': ['${BITBUCKET_COMMIT}'],
    'github': [
        '${GITHUB_SERVER_URL}',
        '/',
        '${GITHUB_REPOSITORY}',
        '/commits/',
        '${GITHUB_SHA}'
    ]
}


class ArtifactGitUrlEnvVar(DefaultedEnvVar):

    def __init__(self, env):
        super().__init__(env, "ARTIFACT_GIT_URL", '')

    def notes(self, ci):
        #return f"{NOTE}. Defaults to {"".join(CI_ENV_VAR_NAMES[ci]))}."
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

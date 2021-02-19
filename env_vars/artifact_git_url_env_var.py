from env_vars import CompositeEnvVar, DefaultedEnvVar

NOTE = "The link to the source git commit this build was based on."

CI_ENV_VARS = {
    'bitbucket': CompositeEnvVar(
        'https://bitbucket.org',
        '/',
        '${BITBUCKET_WORKSPACE}',
        '/{BITBUCKET_REPO_SLUG}',
        '/commits/',
        '${BITBUCKET_COMMIT}'
    ),
    'github': CompositeEnvVar(
        '${GITHUB_SERVER_URL}',
        '/',
        '${GITHUB_REPOSITORY}',
        '/commits/',
        '${GITHUB_SHA}'
    )
}


class ArtifactGitUrlEnvVar(DefaultedEnvVar):

    def __init__(self, env):
        super().__init__(env, "ARTIFACT_GIT_URL", '')

    def notes(self, ci):
        #return f"{NOTE}. Defaults to {CI_ENV_VARS[ci].string)}."
        return NOTE

    @property
    def is_required(self):
        return True  # To keep Docs the same for now

    @property
    def value(self):
        if self.is_set:
            return self.string
        else:
            return CI_ENV_VARS[self.ci].value(self._env)

    @property
    def ci(self):
        # TODO: Look at env-vars...?
        return 'github'

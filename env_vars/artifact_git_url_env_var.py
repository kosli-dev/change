from env_vars import CompoundEnvVar, DefaultedEnvVar

NAME = "MERKELY_ARTIFACT_GIT_URL"
NOTE = "The link to the source git commit this build was based on."


class ArtifactGitUrlEnvVar(DefaultedEnvVar):

    def __init__(self, env):
        super().__init__(env, NAME, '')

    def notes(self, ci):
        #return f"{NOTE}. Defaults to {self.ci_env_var.string}."
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
            'bitbucket': CompoundEnvVar(self._env, self.name,
                'https://bitbucket.org',
                '/',
                '${BITBUCKET_WORKSPACE}',
                '/{BITBUCKET_REPO_SLUG}',
                '/commits/',
                '${BITBUCKET_COMMIT}'
            ),
            'github': CompoundEnvVar(self._env, self.name,
                '${GITHUB_SERVER_URL}',
                '/',
                '${GITHUB_REPOSITORY}',
                '/commits/',
                '${GITHUB_SHA}'
            )
        }[self._ci]

    @property
    def _ci(self):
        # TODO
        # count no of env-vars starting GITHUB_
        # count no of env-vars starting BITBUCKET_
        return 'github'

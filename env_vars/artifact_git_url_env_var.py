from env_vars import CompoundEnvVar, DefaultedEnvVar
import os

NAME = "MERKELY_ARTIFACT_GIT_URL"
NOTE = "The link to the source git commit this build was based on."


class ArtifactGitUrlEnvVar(DefaultedEnvVar):

    def __init__(self, env):
        super().__init__(env, NAME, '')

    def notes(self, ci):
        if ci is 'docker':
            return NOTE
        else:
            return f"{NOTE}. Defaults to {self._ci_env_vars[ci].string}."

    def is_required(self, ci):
        return ci == 'docker'

    @property
    def value(self):
        if self.string != "":
            return self.string
        else:
            return self._ci_env_var.value

    @property
    def _ci_env_var(self):
        return self._ci_env_vars[self._ci]

    @property
    def _ci_env_vars(self):
        return {
            'bitbucket': CompoundEnvVar(self._env, self.name,
                'https://bitbucket.org',
                '/',
                '${BITBUCKET_WORKSPACE}',
                '/',
                '${BITBUCKET_REPO_SLUG}',
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
        }

    @property
    def _ci(self):
        on_github = len(list(key for key in os.environ.keys() if key.startswith('GITHUB_'))) > 0
        if on_github:
            return 'github'
        on_bitbucket = len(list(key for key in os.environ.keys() if key.startswith('BITBUCKET_'))) > 0
        if on_bitbucket:
            return 'bitbucket'
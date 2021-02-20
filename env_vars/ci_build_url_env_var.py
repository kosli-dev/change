import os
from env_vars import CompoundEnvVar, DefaultedEnvVar

NAME = "MERKELY_CI_BUILD_URL"
NOTE = "Link to the build in the ci system."


class CIBuildUrlEnvVar(DefaultedEnvVar):

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
        if self.string != "":
            return self.string
        else:
            return self._ci_env_var.value

    @property
    def _ci_env_var(self):
        return {
            'bitbucket': CompoundEnvVar(self._env, self.name,
                "https://bitbucket.org" ,
                "/",
                "${BITBUCKET_WORKSPACE}",
                "/",
                '${BITBUCKET_REPO_SLUG}',
                "/addon/pipelines/home#!/results/",
                "${BITBUCKET_BUILD_NUMBER}"
            ),
            'github': CompoundEnvVar(self._env, self.name,
                "${GITHUB_SERVER_URL}",
                "/",
                "${GITHUB_REPOSITORY}",
                "/actions/runs/",
                '${GITHUB_RUN_ID}'
            ),
        }[self._ci]

    @property
    def _ci(self):
        on_github = len(list(key for key in os.environ.keys() if key.startswith('GITHUB_'))) > 0
        if on_github:
            return 'github'
        on_bitbucket = len(list(key for key in os.environ.keys() if key.startswith('BITBUCKET_'))) > 0
        if on_bitbucket:
            return 'bitbucket'

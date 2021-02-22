from env_vars import CompoundEnvVar, DynamicEnvVar

NAME = "MERKELY_CI_BUILD_URL"
NOTE = "Link to the build in the ci system."


class CIBuildUrlEnvVar(DynamicEnvVar):

    def __init__(self, env):
        super().__init__(env, NAME, NOTE)

    @property
    def _ci_env_vars(self):
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
        }

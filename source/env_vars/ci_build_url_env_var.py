from env_vars import CompoundEnvVar, CompoundCiEnvVar, CiEnvVar

NAME = "MERKELY_CI_BUILD_URL"
NOTE = "Link to the build in the ci system."


class CIBuildUrlEnvVar(CompoundCiEnvVar):

    def __init__(self, env):
        super().__init__(env, NAME, NOTE)

    @property
    def _ci_env_vars(self):
        return {
            'bitbucket': CompoundEnvVar(
                self._env,
                self.name,
                "https://bitbucket.org" ,
                "/",
                CiEnvVar("BITBUCKET_WORKSPACE"),
                "/",
                CiEnvVar('BITBUCKET_REPO_SLUG'),
                "/addon/pipelines/home#!/results/",
                CiEnvVar("BITBUCKET_BUILD_NUMBER")
            ),
            'github': CompoundEnvVar(
                self._env,
                self.name,
                CiEnvVar("GITHUB_SERVER_URL"),
                "/",
                CiEnvVar("GITHUB_REPOSITORY"),
                "/actions/runs/",
                CiEnvVar('GITHUB_RUN_ID')
            ),
        }

    def doc_example(self, ci_name, _command_name):
        return False, ""

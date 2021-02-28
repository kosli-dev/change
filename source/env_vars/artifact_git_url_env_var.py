from env_vars import CompoundEnvVar, CompoundCiEnvVar, CiEnvVar

NAME = "MERKELY_ARTIFACT_GIT_URL"
NOTE = "The link to the source git commit this build was based on."


class ArtifactGitUrlEnvVar(CompoundCiEnvVar):

    def __init__(self, env):
        super().__init__(env, NAME, NOTE)

    @property
    def _ci_env_vars(self):
        return {
            'bitbucket': CompoundEnvVar(
                self._env,
                self.name,
                'https://bitbucket.org',
                '/',
                CiEnvVar('BITBUCKET_WORKSPACE'),
                '/',
                CiEnvVar('BITBUCKET_REPO_SLUG'),
                '/commits/',
                CiEnvVar('BITBUCKET_COMMIT')
            ),
            'github': CompoundEnvVar(
                self._env,
                self.name,
                CiEnvVar('GITHUB_SERVER_URL'),
                '/',
                CiEnvVar('GITHUB_REPOSITORY'),
                '/commits/',
                CiEnvVar('GITHUB_SHA')
            )
        }

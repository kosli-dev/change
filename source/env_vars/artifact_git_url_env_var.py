from env_vars import CompoundEnvVar, CompoundCiEnvVar, CiEnvVar


class ArtifactGitUrlEnvVar(CompoundCiEnvVar):

    def __init__(self, env):
        super().__init__(env, "MERKELY_ARTIFACT_GIT_URL", '')

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

    def doc_example(self, ci_name, _command_name):
        return False, ""

    def doc_note(self, _ci_name, _command_name):
        return "The link to the source git commit this build was based on."

from env_vars import CompoundEnvVar, DynamicCiEnvVar, CiEnvVar

NAME = "MERKELY_ARTIFACT_GIT_COMMIT"
NOTE = "The sha of the git commit that produced this build."


class ArtifactGitCommitEnvVar(DynamicCiEnvVar):

    def __init__(self, env):
        super().__init__(env, NAME, NOTE)

    @property
    def _ci_env_vars(self):
        return {
            'bitbucket': CompoundEnvVar(self._env, self.name, CiEnvVar('BITBUCKET_COMMIT')),
            'github': CompoundEnvVar(self._env, self.name, CiEnvVar('GITHUB_SHA')),
        }

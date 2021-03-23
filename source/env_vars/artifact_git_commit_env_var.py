from env_vars import CompoundEnvVar, CompoundCiEnvVar, CiEnvVar

NAME = "MERKELY_ARTIFACT_GIT_COMMIT"
NOTE = "The sha of the git commit that produced this build."


class ArtifactGitCommitEnvVar(CompoundCiEnvVar):

    def __init__(self, env):
        super().__init__(env, NAME, NOTE)

    @property
    def _ci_env_vars(self):
        return {
            'bitbucket': CompoundEnvVar(self._env, self.name, CiEnvVar('BITBUCKET_COMMIT')),
            'github': CompoundEnvVar(self._env, self.name, CiEnvVar('GITHUB_SHA')),
        }

    def ci_doc_example(self, ci_name, _command_name):
        return False, ""


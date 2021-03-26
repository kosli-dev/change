from env_vars import CompoundEnvVar, CompoundCiEnvVar, CiEnvVar


class ArtifactGitCommitEnvVar(CompoundCiEnvVar):

    def __init__(self, env):
        super().__init__(env, "MERKELY_ARTIFACT_GIT_COMMIT", '')

    @property
    def _ci_env_vars(self):
        return {
            'bitbucket': CompoundEnvVar(self._env, self.name, CiEnvVar('BITBUCKET_COMMIT')),
            'github': CompoundEnvVar(self._env, self.name, CiEnvVar('GITHUB_SHA')),
        }

    def doc_example(self, _ci_name, _command_name):
        return False, ""

    def doc_note(self, _ci_name, _command_name):
        return "The sha of the git commit that produced this build."


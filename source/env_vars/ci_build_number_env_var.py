from env_vars import CompoundEnvVar, CompoundCiEnvVar, CiEnvVar


class CIBuildNumberEnvVar(CompoundCiEnvVar):

    def __init__(self, env):
        super().__init__(env, "MERKELY_CI_BUILD_NUMBER")

    @property
    def _ci_env_vars(self):
        return {
            'bitbucket': CompoundEnvVar(self._env, self.name, CiEnvVar('BITBUCKET_BUILD_NUMBER')),
            'github': CompoundEnvVar(self._env, self.name, CiEnvVar('GITHUB_RUN_ID')),
        }

    def doc_example(self, _ci_name, _command_name):
        return False, ""

    def doc_note(self, ci_name, _command_name):
        note = "The ci build number."
        cev = self._ci_env_vars
        if ci_name in cev:
            note += f" Defaults to :code:`{cev[ci_name].string}`"
        return note


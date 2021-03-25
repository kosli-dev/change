from env_vars import StaticDefaultedEnvVar


class SrcRepoRootEnvVar(StaticDefaultedEnvVar):

    def __init__(self, env):
        default = "/src"
        notes = " ".join([
            "The directory where the source git repository is volume-mounted.",
            f"Defaults to `{default}`",
        ])
        super().__init__(env, "MERKELY_SRC_REPO_ROOT", default, notes)

    def ci_doc_example(self, ci_name, _command_name):
        if ci_name == 'github':
            return True, "${{ github.workspace }}"
        if ci_name == 'bitbucket':
            return True, "${PWD}"
        return False, ""

from env_vars import StaticDefaultedEnvVar

DEFAULT_DIR = '/src'


class SrcRepoRootEnvVar(StaticDefaultedEnvVar):

    def __init__(self, env):
        super().__init__(env, "MERKELY_SRC_REPO_ROOT", DEFAULT_DIR)

    def doc_example(self, ci_name, _command_name):
        if ci_name == 'github':
            return True, "${{ github.workspace }}"
        if ci_name == 'bitbucket':
            return True, "${PWD}"
        return False, ""

    def doc_note(self, ci_name, _command_name):
        note = " ".join([
            "The directory where the source git repository is volume-mounted.",
            f"Defaults to `{DEFAULT_DIR}`.",
        ])
        if ci_name == 'github':
            note += " ".join([
                "In a github uses: directive the repo directory is",
                "automatically volume-mounted to ${{ github.workspace }}."
            ])
        return note

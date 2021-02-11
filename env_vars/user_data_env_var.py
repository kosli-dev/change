from commands import load_json
from env_vars import DefaultedEnvVar

DESCRIPTION = "\n".join([
    "If provided, a filename whose json content to embed in the deployment.",
    "The filename must be volume-mounted in the container.",
    "If not provided, defaults to an empty json Hash '{}'",
])


class UserDataEnvVar(DefaultedEnvVar):

    def __init__(self, env):
        super().__init__(env, "MERKELY_USER_DATA", None, DESCRIPTION)

    @property
    def value(self):
        filename = super().value
        if filename is None or filename == "":
            return self.default
        else:
            return load_json(filename)

    @property
    def default(self):
        return {}

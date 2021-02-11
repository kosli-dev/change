from commands import load_json
from env_vars import DefaultedEnvVar

DESCRIPTION = "\n".join([
    "If provided, a filename whose json content to embed in the deployment.",
    "The filename must be volume-mounted in the container.",
    "If not provided, defaults to an empty json Hash '{}'",
])


class UserDataEnvVar(DefaultedEnvVar):

    def __init__(self, env):
        default = '{}'
        super().__init__(env, "MERKELY_USER_DATA", default, DESCRIPTION)

    @property
    def value(self):
        if self.is_set:
            filename = super().value
            return load_json(filename)
        else:
            return self.default


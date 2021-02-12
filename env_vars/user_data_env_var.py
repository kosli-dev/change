from commands import load_json
from env_vars import DefaultedEnvVar

DEFAULT = {}

NOTES = "\n".join([
    "If provided, a filename whose json content to embed in the deployment.",
    "The filename must be volume-mounted in the container.",
    f"If not provided, defaults to {DEFAULT}",
])


class UserDataEnvVar(DefaultedEnvVar):

    def __init__(self, env):
        super().__init__(env, "USER_DATA", NOTES)

    @property
    def value(self):
        if self._is_set:
            filename = super().value
            return load_json(filename)
        else:
            return DEFAULT

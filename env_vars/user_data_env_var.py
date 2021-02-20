from env_vars import DefaultedEnvVar

DEFAULT = {}

NOTES = "\n".join([
    "If provided, a filename whose json content to embed in the deployment.",
    "The filename must be volume-mounted in the container.",
    f"If not provided, defaults to {DEFAULT}",
])


class UserDataEnvVar(DefaultedEnvVar):

    def __init__(self, env):
        super().__init__(env, "MERKELY_USER_DATA", NOTES)

    @property
    def value(self):
        if self.string != "":
            from commands import load_json
            filename = self.string
            return load_json(filename)
        else:
            return DEFAULT

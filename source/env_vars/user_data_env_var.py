from env_vars import DefaultedEnvVar

DEFAULT = {}

NOTES = "\n".join([
    "If provided, a filename whose json content to embed in the deployment.",
    "The filename must be volume-mounted in the container.",
    f"If not provided, defaults to {DEFAULT}",
])


class UserDataEnvVar(DefaultedEnvVar):

    def __init__(self, external):
        super().__init__(external.env, "MERKELY_USER_DATA", NOTES)
        self._external = external

    @property
    def value(self):
        if self.string != "":
            filename = self.string
            return self._external.load_json(filename)
        else:
            return DEFAULT

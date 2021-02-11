from env_vars import DefaultedEnvVar

DEFAULT = "UNDEFINED"

NOTES = "\n".join([
    f"Defaults to {DEFAULT}",
])


class DescriptionEnvVar(DefaultedEnvVar):

    def __init__(self, env):
        super().__init__(env, "MERKELY_DESCRIPTION", NOTES)

    @property
    def value(self):
        if self._is_set:
            return super().value
        else:
            return DEFAULT

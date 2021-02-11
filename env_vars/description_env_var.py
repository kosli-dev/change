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
        description = super().value
        if description is None or description == "":
            return DEFAULT
        else:
            return description

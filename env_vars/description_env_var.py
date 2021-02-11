from env_vars import StaticDefaultedEnvVar

DEFAULT = "UNDEFINED"

NOTES = "\n".join([
    f"Defaults to {DEFAULT}",
])


class DescriptionEnvVar(StaticDefaultedEnvVar):

    def __init__(self, env):
        super().__init__(env, "MERKELY_DESCRIPTION", DEFAULT, NOTES)

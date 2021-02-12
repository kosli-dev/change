from env_vars import StaticDefaultedEnvVar

DEFAULT = "https://app.compliancedb.com"

NOTES = "\n".join([
    f"Defaults to {DEFAULT}",
])


class HostEnvVar(StaticDefaultedEnvVar):

    def __init__(self, env):
        super().__init__(env, "HOST", DEFAULT, NOTES)

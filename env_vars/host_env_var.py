from env_vars import DefaultedEnvVar

DEFAULT = "https://app.compliancedb.com"

NOTES = "\n".join([
    f"Defaults to {DEFAULT}",
])


class HostEnvVar(DefaultedEnvVar):

    def __init__(self, env):
        super().__init__(env, "MERKELY_HOST", NOTES)

    @property
    def value(self):
        host = super().value
        if host is None or host == "":
            return DEFAULT
        else:
            return host

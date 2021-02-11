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
        if self._is_set:
            return super().value
        else:
            return DEFAULT

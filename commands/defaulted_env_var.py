from .env_var import EnvVar


class DefaultedEnvVar(EnvVar):
    def __init__(self, command, name, default, description):
        super().__init__(command, name, description)
        self._default = default

    @property
    def value(self):
        return self._env.get(self.name, self._default)

    @property
    def default(self):
        return self._default

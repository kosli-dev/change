from .env_var import EnvVar


class DefaultedEnvVar(EnvVar):
    def __init__(self, name, env, default, description):
        super().__init__(name, env, description)
        self._default = default
        self._value = self._env.get(self.name, self._default)

    @property
    def default(self):
        return self._default

    @property
    def value(self):
        return self._value

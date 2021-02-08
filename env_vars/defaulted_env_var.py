from env_vars import EnvVar


class DefaultedEnvVar(EnvVar):

    def __init__(self, env, name, default, description):
        super().__init__(env, name, description)
        self._default = default

    @property
    def value(self):
        return self.env.get(self.name, self._default)

    @property
    def default(self):
        return self._default

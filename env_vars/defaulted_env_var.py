from env_vars import EnvVar


class DefaultedEnvVar(EnvVar):
    """
    A defaulted OS environment-variable.
    """
    def __init__(self, env, name, default, description):
        super().__init__(env, name, description)
        self._default = default

    @property
    def type(self):
        return 'defaulted'

    @property
    def value(self):
        return self.env.get(self.name, self.default)

    @property
    def is_set(self):
        return self.env.get(self.name) is not None

    @property
    def default(self):
        return self._default
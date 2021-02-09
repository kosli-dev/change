from env_vars import EnvVar


class DefaultedEnvVar(EnvVar):
    """
    Represents a defaulted OS environment-variable.
    Contributes something to its parent Command's http payload.
    The default is supplied at construction, and is used
    as its value if it does not exist at runtime.
    """
    def __init__(self, env, name, default, description):
        super().__init__(env, name, description)
        self._default = default

    @property
    def type(self):
        return 'defaulted'

    @property
    def value(self):
        return self.env.get(self.name, self._default)

    @property
    def default(self):
        return self._default

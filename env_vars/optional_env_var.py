from env_vars import EnvVar


class OptionalEnvVar(EnvVar):
    """
    Represents an optional OS environment-variable.
    If not present at runtime, does not contribute to
    its parent Command's http payload
    """
    def __init__(self, env, name, description):
        super().__init__(env, name, description)

    @property
    def type(self):
        return 'optional'

    @property
    def value(self):
        return self.env.get(self.name, None)

    @property
    def is_present(self):
        return self.value is not None

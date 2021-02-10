from env_vars import EnvVar


class OptionalEnvVar(EnvVar):
    """
    Represents an optional OS environment-variable that,
    if not present at runtime, does not contribute to
    its parent Command's http payload.
    """
    def __init__(self, env, name, description):
        super().__init__(env, name, description)

    @property
    def type(self):
        return 'optional'

    @property
    def value(self):
        """
        The OS env-var for name if present, otherwise None.
        """
        return self.env.get(self.name, None)

    @property
    def is_set(self):
        return self.value is not None

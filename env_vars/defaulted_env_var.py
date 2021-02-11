from env_vars import EnvVar


class DefaultedEnvVar(EnvVar):
    """
    A defaulted OS environment-variable.
    """
    def __init__(self, env, name, notes):
        super().__init__(env, name, notes)

    @property
    def is_required(self):
        return False

    @property
    def value(self):
        return self.env.get(self.name, None)

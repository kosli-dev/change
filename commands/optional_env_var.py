from commands import EnvVar


class OptionalEnvVar(EnvVar):
    def __init__(self, env, name, description):
        super().__init__(env, name, description)

    @property
    def value(self):
        return self.env.get(self.name, None)

    @property
    def is_present(self):
        return self.value is not None

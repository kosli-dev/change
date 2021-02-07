from commands import EnvVar


class OptionalEnvVar(EnvVar):
    def __init__(self, command, name, description):
        super().__init__(command, name, description)

    @property
    def value(self):
        return self._env.get(self.name, None)

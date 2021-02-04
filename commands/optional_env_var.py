from commands import EnvVar


class OptionalEnvVar(EnvVar):
    def __init__(self, name, env, description):
        super().__init__(name, env, description)

    @property
    def value(self):
        return self._env.get(self.name, None)


class OptionalEnvVar:
    def __init__(self, name, env):
        self._name = name
        self._env = env

    @property
    def name(self):
        return f"MERKELY_{self._name}"

    def verify(self):
        self.value

    @property
    def value(self):
        return self._env.get(self.name, None)

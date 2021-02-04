
class EnvVar:
    def __init__(self, name, env, description):
        self._name = name
        self._env = env
        self._description = description

    @property
    def name(self):
        return self._name

    @property
    def description(self):
        return self._description

    def verify(self):
        self.value
        return self

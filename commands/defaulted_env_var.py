
class DefaultedEnvVar:
    def __init__(self, name, env, default):
        self._name = name
        self._env = env
        self._default = default

    @property
    def name(self):
        return self._name

    @property
    def value(self):
        return self._env.get(self.name, self._default)

    def verify(self):
        return self


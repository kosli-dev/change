
class EnvVar:
    def __init__(self, env, name, description):
        self._env = env
        self._name = name
        self._description = description

    @property
    def value(self):
        raise NotImplementedError(f"{self.__class__.__name__}.value override missing")

    @property
    def name(self):
        return self._name

    @property
    def description(self):
        return self._description

    @property
    def env(self):
        return self._env

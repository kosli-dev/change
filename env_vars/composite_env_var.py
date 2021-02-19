
class CompositeEnvVar:
    def __init__(self, *parts):
        self._parts = parts

    @property
    def string(self):
        return "".join(self._parts)

    @property
    def value(self, env):
        return "X"

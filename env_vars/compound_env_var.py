
class CompoundEnvVar:
    def __init__(self, *parts):
        """
        The parts are all strings and come in two forms:
        'plain-string' and '${ENV_VAR}'.
        The latter are expanded at run-time in value().
        The concatenated parts have a format designed for living documentation.
        """
        self._parts = parts

    @property
    def string(self):
        return "".join(self._parts)

    @property
    def value(self, env):
        return "TODO"


class EnvVar:
    def __init__(self, command, name, description):
        self._command = command
        self._name = name
        self._description = description

    @property
    def value(self):
        raise NotImplementedError("EnvVar value override missing")

    @property
    def name(self):
        return self._name

    @property
    def description(self):
        return self._description

    @property
    def _env(self):
        return self._command._context.env

from errors import ChangeError
from env_vars import CiEnvVar


class CompoundEnvVar:
    def __init__(self, env, name, *parts):
        """
        The parts are all strings and come in two forms:
        'string' and CiEnvVar.
        The latter are expanded at run-time in value().
        The concatenated parts have a format designed for living documentation.
        """
        self._env = env
        self._name = name
        self._parts = parts

    @property
    def name(self):
        return self._name

    @property
    def string(self):
        return "".join(str(part) for part in self._parts)

    @property
    def value(self):
        return "".join(self._expand(part) for part in self._parts)

    @property
    def names(self):
        return list(part.string for part in self._parts if isinstance(part, CiEnvVar))

    def _expand(self, part):
        if isinstance(part, CiEnvVar):
            return self._expanded(part)
        else:
            return part

    def _expanded(self, part):
        value = part.value(self._env)
        if value is None:
            message = f"environment-variable {self.name} defaults to `{self.string}` but `{part.string}` is not set."
            raise ChangeError(message)
        return value

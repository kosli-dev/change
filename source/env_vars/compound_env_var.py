from errors import ChangeError


class CompoundEnvVar:
    def __init__(self, env, name, *parts):
        """
        The parts are all strings and come in two forms:
        'plain-string' and '${ENV_VAR}'.
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

    def _expand(self, part):
        if part.startswith('${') and part.endswith('}'):
            return self._expand_env_var(part)
        else:
            return part

    def _expand_env_var(self, part):
        name = part[2:-1]
        expanded = self._env.get(name, None)
        if expanded is None:
            message = f"environment-variable {self.name} defaults to `{self.string}` but `{name}` is not set."
            raise ChangeError(message)
        return expanded


class EnvVar:
    """
    An abstract base class for 'smart' OS env-vars.
    """
    def __init__(self, env, name, description):
        assert name is not None
        assert name != ""
        assert description is not None
        assert description != ""
        self._env = env
        self._name = name
        self._description = description

    @property
    def name(self):
        """
        Non-empty string, as set in the ctor.
        Used in living documentation.
        Never raises.
        """
        return self._name

    @property
    def type(self):
        """
        Non-empty string.
        Used in living documentation.
        Never raises.
        """
        raise NotImplementedError(f"{self.__class__.__name__}.type override missing")

    @property
    def description(self):
        """
        Non-empty string as set in the ctor.
        Used in living documentation.
        Never raises.
        """
        return self._description

    @property
    def value(self):
        """
        run() validates its command by getting the property
        of each command's env-var. Each command's env-var will
        raise if it is invalid.
        """
        raise NotImplementedError(f"{self.__class__.__name__}.value override missing")

    @property
    def env(self):
        """
        The underlying OS environment.
        """
        return self._env

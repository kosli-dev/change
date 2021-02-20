from abc import ABC, abstractmethod


class EnvVar(ABC):
    """
    An abstract base class for 'smart' OS environment-variables.
    """
    def __init__(self, env, name, notes, example=None):
        assert name is not None
        assert name != ""
        self.__env = env
        self.__name = name
        self.__notes = notes
        if example is None:
            example = "${...}"
        self.__example = example

    @property
    def _env(self):
        return self.__env

    def _get(self, *, name=None, default):
        if name is None:
            name = self.name
        return self.__env.get(name, default)

    @property
    def is_empty(self):
        """
        Returns true if the environment-variable is set to
        the empty string. This can easily happen in a docker
        command when you miss-type a --env option!
        """
        return self.string == ""

    @property
    def string(self):
        """
        Returns the string as set in the environment-variable,
        or the empty-string if not set.
        """
        return self._get(default="")

    @property
    def is_set(self):
        """
        Returns true if this environment-variable is set.
        Note: returns false if the environment-variable
        is set, but to the empty string.
        """
        return self._get(default=None) is not None

    @property
    def name(self):
        """
        Returns the name of the environment-variable, as set in the ctor.
        Used in living documentation. Never raises.
        """
        return self.__name

    def notes(self, ci):
        """
        Returns notes string.
        Uses either the value set in the ctor,
        or override can inspect ci parameter.
        Used in living documentation. Never raises.
        """
        return self.__notes

    @property
    def example(self):
        return self.__example

    @property
    @abstractmethod
    def is_required(self):
        """
        Returns True or False.
        Used in living documentation. Never raises.
        """

    @property
    @abstractmethod
    def value(self):
        """
        Subclasses must raise if their value is invalid.
        run() validates its command by getting the value property
        of each command's env-var.
        """

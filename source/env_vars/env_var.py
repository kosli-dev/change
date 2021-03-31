from abc import ABC, abstractmethod


class EnvVar(ABC):
    """
    An abstract base class for 'smart' OS environment-variables.
    """
    def __init__(self, env, name):
        assert name is not None
        assert name != ""
        self.__env = env
        self.__name = name

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
    @abstractmethod
    def is_required(self, ci):
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

    #- - - - - - - - - - - - - - - - - - - - - - -
    # Living documentation

    @property
    def name(self):
        """
        Returns the name of the environment-variable, as set in the c'tor.
        Used in living documentation. Never raises.
        """
        return self.__name

    @abstractmethod
    def doc_example(self, ci_name, command_name):
        """
        Used in living documentation. Never raises.
        See docs.merkely.com/source/docs/doc_txt.py
        """

    @abstractmethod
    def doc_note(self, ci_name, command_name):
        """
        Used in living documentation. Never raises.
        See docs.merkely.com/source/_ext/describe_command.py
        """

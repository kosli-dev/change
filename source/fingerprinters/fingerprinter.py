from abc import ABC, abstractmethod


class Fingerprinter(ABC):

    @property
    @abstractmethod
    def notes(self):
        """
        """

    @property
    @abstractmethod
    def example(self):
        """
        """

    @abstractmethod
    def handles_protocol(self, string):
        """
        Returns True iff string starts with the class's protocol.
        """

    @abstractmethod
    def artifact_name(self, string):
        """
        Returns the artifact_name from after the protocol string.
        Raises if handles_protocol(string) is False.
        """

    @abstractmethod
    def artifact_basename(self, string):
        """
        Returns the artifact_basename from after the protocol string.
        Raises if handles_protocol(string) is False.
        """

    @abstractmethod
    def sha(self, protocol, artifact_name):
        """
        Returns the sha for the artifact_name.
        Raises if handles_protocol(string) is False.
        """

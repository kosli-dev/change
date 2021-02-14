from abc import ABC


class Fingerprinter(ABC):

    def handles_protocol(self, string):  # pragma: no cover
        raise NotImplementedError()

    def artifact_name(self, string):  # pragma: no cover
        raise NotImplementedError()

    def artifact_basename(self, string):  # pragma: no cover
        raise NotImplementedError()

    def sha(self, protocol, artifact_name):  # pragma: no cover
        raise NotImplementedError()

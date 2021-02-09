
class Fingerprinter:

    def __call__(self, protocol, artifact_name):
        print(self._calculating_message(protocol, artifact_name))
        sha256 = self._fingerprint(artifact_name)
        print(self._calculated_message(sha256))
        return sha256

    def _fingerprint(self, artifact_name):
        raise NotImplementedError(f"{self._class_name}._fingerprint(...) subclass override missing")

    @staticmethod
    def _calculating_message(protocol, artifact_name):
        return f"Calculating fingerprint for {protocol}{artifact_name}"

    @staticmethod
    def _calculated_message(sha256):
        return f"Calculated fingerprint: {sha256}"

    @property
    def _class_name(self):
        return self.__class__.__name__


class Fingerprinter:

    def __call__(self, protocol, artifact_name):
        print(self._calculating_message(protocol, artifact_name))
        sha256 = self._fingerprint(artifact_name)
        print(self._calculated_message(sha256))
        return sha256

    def _fingerprint(self, artifact_name):  # pragma: no cover
        raise NotImplementedError

    @staticmethod
    def _calculating_message(protocol, artifact_name):
        return f"Calculating fingerprint for {protocol}{artifact_name}"

    @staticmethod
    def _calculated_message(sha256):
        return f"Calculated fingerprint: {sha256}"

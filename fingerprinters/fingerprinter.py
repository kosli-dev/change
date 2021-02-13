
class Fingerprinter:

    def __call__(self, protocol, artifact_name):
        sha256 = self._fingerprint(artifact_name)
        return sha256

    def _fingerprint(self, artifact_name):  # pragma: no cover
        raise NotImplementedError

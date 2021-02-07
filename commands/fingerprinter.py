
class Fingerprinter:

    def __call__(self, protocol, image_name):
        print(self._calculating_message(protocol, image_name))
        repo_digest = self._fingerprint(image_name)
        print(self._calculated_message(repo_digest))
        return repo_digest

    def _calculating_message(self, protocol, artifact_name):
        return f"Calculating fingerprint for {protocol}{artifact_name}"

    @staticmethod
    def _calculated_message(sha):
        return f"Calculated fingerprint: {sha}"

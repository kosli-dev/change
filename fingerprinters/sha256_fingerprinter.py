from fingerprinters import Fingerprinter

PROTOCOL = 'sha256://'


class Sha256Fingerprinter(Fingerprinter):

    @property
    def notes(self):
        return "\n".join([
            f"The string `{PROTOCOL}` followed by the artifact's 64 character sha256, then `/`, then it's non-empty name."
            'Example:',
            'docker run ... \\',
            f'    --env MERKELY_FINGERPRINT=”{PROTOCOL}${{YOUR_ARTIFACT_SHA256}}/${{YOUR_ARTIFACT_NAME}}” \\',
            '    ...',
        ])

    def sha(self, _protocol, artifact_name):
        pass
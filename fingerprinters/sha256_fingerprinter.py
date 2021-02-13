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

    def _fingerprint(self, pathed_filename):
        # Mocked in /tests/unit/utils/mock_file_fingerprinter.py
        # openssl is an Alpine package installed in /Dockerfile
        output = subprocess.check_output(["openssl", "dgst", "-sha256", '/'+pathed_filename])
        digest_in_bytes = output.split()[1]
        return digest_in_bytes.decode('utf-8')

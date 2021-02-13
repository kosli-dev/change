from fingerprinters import Fingerprinter
import os
import subprocess

PROTOCOL = 'file://'


class FileFingerprinter(Fingerprinter):

    @property
    def notes(self):
        return "\n".join([
            f'The string `{PROTOCOL}` followed by the full path of the file to fingerprint.',
            'The full path must be volume-mounted.',
            'Example:',
            'docker run ... \\',
            f'    --env MERKELY_FINGERPRINT=”{PROTOCOL}${{YOUR_FILE_PATH}} \\',
            '    --volume=${YOUR_FILE_PATH}:${YOUR_FILE_PATH} \\',
            '    ...',
        ])

    def artifact_name(self, s):
        return s

    def artifact_basename(self, s):
        return os.path.basename(s)

    def sha(self, _protocol, pathed_filename):
        # Mocked in /tests/unit/utils/mock_file_fingerprinter.py
        # openssl is an Alpine package installed in /Dockerfile
        output = subprocess.check_output(["openssl", "dgst", "-sha256", '/'+pathed_filename])
        digest_in_bytes = output.split()[1]
        return digest_in_bytes.decode('utf-8')
